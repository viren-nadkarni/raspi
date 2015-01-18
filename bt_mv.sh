#!/bin/bash

IFS="
"
source_path="/home/pi/bittorrent/download"

destination_host="Inspiron.local"
destination_path="."

ftp_user="pi"
ftp_pass="Aq1sw2de"

files=$(ls -A $source_path)
torrents=$(transmission-remote 9091 --list | sed -e '1d;$d;s/^ *//' | cut --only-delimited --delimiter " " --fields 1)

# Remove completed and stopped torrents from transmission
for torrent in $torrents; do
    is_completed=$(transmission-remote 9091 --torrent $torrent --info | grep "Percent Done: 100%")
    is_stopped=$(transmission-remote 9091 --torrent $torrent --info | grep "State: Seeding\|Stopped\|Finished\|Idle")

    if [ "$is_completed" ] && [ "$is_stopped" ]; then
        transmission-remote 9091 --torrent $torrent --remove && echo "Removed torrent:$torrent from transmission"
    fi
done

if [ ! "$files" ]; then
    echo "Nothing to transfer"
    exit 0
fi

# Check if dest is online
if ! (ping -c 1 $destination_host > /dev/null 2>&1); then
    echo "$destination_host seems offline"
    exit 1
fi

# ftp to dest and rm local
for file in $files; do
    ncftpput -u $ftp_user -p $ftp_pass -R -v $destination_host $destination_path "$source_path/$file" && rm -rf "$source_path/$file"
    [ $? -eq 0 ] && echo "Moved $file"
done
