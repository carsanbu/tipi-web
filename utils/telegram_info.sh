#!/bin/sh

IP=$(curl http://ipecho.net/plain;)
IIP=$(/sbin/ifconfig $1 | grep "inet addr" | awk -F: '{print $2}' | awk '{print$

/home/pi/tg/telegram -k /home/pi/tg/tg.pub <<STDIN
msg user#12278757 Esta es mi IP externa: $IP 
msg user#12278757 Esta es mi IP interna: $IIP
safe_quit
STDIN

exit 0




