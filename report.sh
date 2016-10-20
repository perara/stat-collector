

server="graylog.grm.sysx.lan"
port=12201
data=`/usr/bin/python collector.py`

http_port=12202

if [ $1 = "tcp" ]; then
  echo "$data"
elif [ $1 = "udp" ]; then
  echo "$data\0" | nc -w 1 -u graylog.grm.sysx.lan 12201
elif [ $1 = "http" ]; then
  curl -XPOST http://graylog.grm.sysx.lan:12202/gelf -p0 -d "$data"
else
  echo "Not a valid transport protocol"
fi


#echo /usr/bin/python collector.py | curl -XPOST http://graylog.grm.sysx.lan:80/gelf -p0 -d @-
