import os
import json
import subprocess
import sys
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
output = subprocess.check_output([sys.executable, os.path.join(PATH, "collector.py")])
obj = json.loads(output.decode())

for item in obj:
    url = "http://%s:%s/gelf" % (config["reporting"]["url"], config["reporting"]["port"])
    data = json.dumps(item)
    req = Request(url, data.encode('utf-8'), {'Content-Type': 'application/json'})
    response = urlopen(req)
    print(response.read())

