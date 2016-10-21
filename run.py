import os
import json
import subprocess
import sys
import time
try:
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
except ImportError:
    from urlparse import urlparse
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError

# Load configuration
PATH = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(PATH, "config.json")) as data_file:
    config = json.load(data_file)

# Run collector.py
start = time.time()
output = subprocess.check_output([sys.executable, os.path.join(PATH, "collector.py")])
obj = json.loads(output.decode())



# Graylog
if config["reporting"]["engine"] == "elasticsearch":

    for item in obj:
        url = "http://%s:%s/gelf" % (config["reporting"]["url"], config["reporting"]["port"])
        print(url)
        data = json.dumps(item)
        req = Request(url, data.encode('utf-8'), {'Content-Type': 'application/json'})
        response = urlopen(req)
        print(response.read())

elif config["reporting"]["engine"] == "influxdb":
    for item in obj:

        for key in item:
            if key == "timestamp" or key == "name": # Blacklisted
                continue

            if "disk_" in key:
                _key = key.replace("disk_", "")
                _type = _key.rsplit('_', 1)[1]
                _key = _key.split("_")[0]

                point = "%s,host=%s,device=%s,type=%s value=%s %s" % ("disk", item["name"],_key, _type, item[key], item["timestamp"])

            elif "memory_" in key:
                _type = key.replace("memory_", "")
                point = "%s,host=%s,type=%s value=%s %s" % ("memory", item["name"],_type, item[key], item["timestamp"])
            elif "network_" in key:
                    _splt = key.split("_")
                    _key = _splt[0]
                    _device = _splt[1]
                    _direction = _splt[2]
                    point = "%s,host=%s,device=%s,direction=%s value=%s %s" % (_key, item["name"],_device, _direction, item[key], item["timestamp"])
            else:
                try:
                    point = "%s,host=%s value=%s %s" % (key, item["name"], int(item[key]), item["timestamp"])
                except:
                    point = "%s,host=%s value=\"%s\" %s" % (key, item["name"], item[key], item["timestamp"])
            print(point)

            url = "http://%s:%s%s" % (config["reporting"]["url"], config["reporting"]["port"], config["reporting"]["prefix"])
            print(url)
            req = Request(url, point.encode('utf-8'))
            req.add_header('Content-Length', '%d' % len(point))
            req.add_header('Content-Type', 'application/octet-stream')
            res = urlopen(req)

        """
        url = "http://%s:%s/gelf" % (config["reporting"]["url"], config["reporting"]["port"])
        print(url)
        data = json.dumps(item)
        req = Request(url, data.encode('utf-8'), {'Content-Type': 'application/json'})
        response = urlopen(req)
        print(response.read())
        """

