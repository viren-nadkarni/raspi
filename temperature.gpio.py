#!/usr/bin/env python

import sys
import os
import time
import datetime
import glob
import plotly.plotly as plotly
from plotly.graph_objs import *
import mysql.connector
import Adafruit_DHT
import RPi.GPIO as gpio

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


def stream_to_plotly(ds_temp, dht_temp, dht_humd, now):
# TODO
# use ploty streaming instead of rebuilding everytime
    import plotly_init


def raw_read_ds18b20():
    base_dir = '/sys/bus/w1/devices/'
    dev_dir = glob.glob(base_dir + '28*')[0]
    dev_file = dev_dir + '/w1_slave'

    f = open(dev_file, 'r')
    lines = f.readlines()
    f.close()

    return lines


def read_ds():
    """Read DS18B20 and return temperature in degree celsius"""
    lines = raw_read_ds18b20()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = raw_read_ds18b20()
    eq_pos = lines[1].find('t=')
    if eq_pos != -1:
        temp = lines[1][eq_pos+2:]
        return float(temp) / 1000.0


def read_dht(pin):
    return Adafruit_DHT.read_retry(11, pin)

def save_to_db(_ds_temp=None, _dht_temp=None, _dht_humd=None):
    cnx = mysql.connector.connect(user='root', database='temp')
    cur = cnx.cursor()
    now = time.time()

    if _ds_temp:
        cur.execute('INSERT INTO ds VALUES (%f, %f)'%(now, _ds_temp))
    if _dht_temp and _dht_humd:
        cur.execute('INSERT INTO dht VALUES (%f, %f, %f)'%(now, _dht_temp, _dht_humd))

    cnx.commit()
    cur.close()
    cnx.close()
    stream_to_plotly(_ds_temp, _dht_temp, _dht_humd, now)


def main():
    ds_temp = None
    dht_humd = None
    dht_temp = None

    try:
        ds_temp = read_ds()
        print 'DS18B20:', ds_temp, u'\xb0C'
    except Exception as e:
        sys.stderr.write(e.message + '\n')

    try:
        dht_humd, dht_temp = read_dht(14)
        print 'DHT11:', dht_temp, u'\xb0C', dht_humd, '%'
    except Exception as e:
        sys.stderr.write(e.message + '\n')

    save_to_db(ds_temp, dht_temp, dht_humd)


if __name__ == '__main__':
    main()
