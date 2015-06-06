echo url="https://www.duckdns.org/update?domains=viren&token=$(cat ~/.duckdns_token)&ip=" | curl -k -o /home/pi/scripts/duckdns/duck.log -K -
