import os
import json
import subprocess
import sys
import time
from loaders import load_config
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
config = load_config()

# Run collector.py
start = time.time()
output = subprocess.check_output([sys.executable, os.path.join(PATH, "collector.py")])
data = json.loads(output.decode())


# Graylog
if config["reporting"]["engine"] == "elasticsearch":

    for item in data:
        url = "http://%s:%s/gelf" % (config["reporting"]["url"], config["reporting"]["port"])
        print(url)
        data = json.dumps(item)
        req = Request(url, data.encode('utf-8'), {'Content-Type': 'application/json'})
        response = urlopen(req)
        print(response.read())

elif config["reporting"]["engine"] == "influxdb":
    url = "http://%s:%s%s" % (config["reporting"]["url"], config["reporting"]["port"], config["reporting"]["prefix"])
    for host_items in data:
        for item in host_items:
            req = Request(url, item.encode('utf-8'))
            req.add_header('Content-Length', '%d' % len(item))
            req.add_header('Content-Type', 'application/octet-stream')
            res = urlopen(req)
            print(item)

        print("Pushed %s points for a host" % (len(host_items)))

    print("-----------------------------")
