#!/bin/bash

echo 'Do not run as script'
exit 1

usermod -m -d /home/viren pi
usermod -l viren pi
groupmod -n viren pi
ln -s /home/viren/ /home/pi
visudo

echo -e '\n' >> /etc/apt/sources.list
echo -e '\ndeb http://archive.raspbian.org/raspbian wheezy main contrib non-free' >> /etc/apt/sources.list
echo -e '\ndeb-src http://archive.raspbian.org/raspbian wheezy main contrib non-free' >> /etc/apt/sources.list

apt-get update

apt-get remove --purge wolfram-engine penguinspuzzle scratch dillo squeak-vm squeak-plugins-scratch sonic-pi idle idle3 netsurf-gtk netsurf-common

apt-get remove --purge gnome-* lxde* lightdm* xserver* desktop-* lxappearance lxinput lxmenu-data lxpanel lxpolkit lxrandr lxsession lxsession-edit lxshortcut lxtask lxterminal leafpad menu menu-xdg xpdf xkb-data xinit xfonts-utils xfonts-encodings xdg-utils xauth xarchiver x11-utils x11-common

apt-get autoremove

apt-get clean

apt-get install -y avahi-daemon colordiff transmission build-essential cython python python-dev python-ipy git apache2 mysql-server samba ncftp vim locate


a2enmod ssl proxy_http 
