#!/usr/bin/env python
import time
import datetime
import mysql.connector
import plotly.plotly as plotly
from plotly.graph_objs import *

username = 'vn14'
api_key = 'e77nnrfnut'
stream_token = open('/home/viren/.plotly_token', 'r').read().strip()

cnx = mysql.connector.connect(user='root', database='temp')
cur = cnx.cursor()

ds_x = list()
ds_y = list()

dht_x = list()
dht_y1 = list()
dht_y2 = list()

now = time.time() - 86400*2
# TODO
# optimize, send only recent entries.
# also, sort database results
cur.execute('SELECT * FROM ds WHERE time > %s ORDER BY time ASC' % (now))
for time, temp in cur:
    strtime = datetime.datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')
    ds_x.append(strtime)
    ds_y.append(temp)

cur.execute('SELECT * FROM dht WHERE time > %s ORDER BY time ASC' % (now))
for time, temp, humd in cur:
    strtime = datetime.datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')
    dht_x.append(strtime)
    dht_y1.append(temp)
    dht_y2.append(humd)

plotly.sign_in(username, api_key)

# outdoor temperature
trace_ds = Scatter(
            x=ds_x,
            y=ds_y,
            mode='lines',
            name='Outdoor Temperature',
            line=Line(shape='spline', color='rgb(44,160,44)'),
            stream=Stream(token=stream_token, maxpoints=200)
)

# indoor temperature
trace_dht1 = Scatter(
            x=dht_x,
            y=dht_y1,
            mode='lines',
            name='Indoor Temperature',
            line=Line(shape='spline', color='rgb(31,119,180)'),
            error_y=ErrorY(type='constant', value=2, color='rgb(109,158,235)', thickness=0.5, visible=True),
            stream=Stream(token=stream_token, maxpoints=200)
)

# indoor humidity
trace_dht2 = Scatter(
            x=dht_x,
            y=dht_y2,
            yaxis='y2',
            mode='lines',
            name='Indoor Humidity',
            line=Line(shape='spline', color='rgb(102,102,102)'),
            error_y=ErrorY(type='constant', value=5, color='rgb(170,170,170)', thickness=0.5, visible=True),
            stream=Stream(token=stream_token, maxpoints=200)
)
dat = Data([trace_ds, trace_dht1, trace_dht2])
lay = Layout(title='weather',
        showlegend=True,
        autosize=True,
        xaxis=XAxis(
            title='Date/Time',
            type='date'),
        yaxis=YAxis(
            title='Temperature C',
            type='linear'),
        yaxis2=YAxis(
            title='Humidity %',
            type='linear',
            overlaying='y',
            side='right'
            )
)

fig = Figure(data=[trace_ds, trace_dht1, trace_dht2], layout=lay)
print plotly.plot(fig, filename='weather')
