#!/bin/bash

apt-get remove --purge wolfram-engine penguinspuzzle scratch dillo squeak-vm squeak-plugins-scratch sonic-pi idle idle3 netsurf-gtk netsurf-common

apt-get remove --purge gnome-* lxde* lightdm* xserver* desktop-* lxappearance lxinput lxmenu-data lxpanel lxpolkit lxrandr lxsession lxsession-edit lxshortcut lxtask lxterminal leafpad menu menu-xdg xpdf xkb-data xinit xfonts-utils xfonts-encodings xdg-utils xauth xarchiver x11-utils x11-common

apt-get autoremove

apt-get clean
