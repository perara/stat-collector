import json
import time
import os
from importlib import import_module
from threading import Thread

PATH = os.path.dirname(os.path.abspath(__file__))
MODULES_PATH = PATH + "/modules/"

result = []  # All results

# Load configuration
with open(os.path.join(PATH, "config.json")) as data_file:
	config = json.load(data_file)

# Set timestamp in the base document
config["global"]["base_document"]["timestamp"] = int(time.time())

def worker(address, host):
	output = config["global"]["base_document"]

	host["address"] = address # Workaround to get address into executor without passing extra param

	for module in os.listdir(MODULES_PATH):
		if ".py" not in module:
			continue

		mod = import_module("modules." + module.replace(".py",""))
		mod.run(host, config, output)

	result.append(output)

threads = []
for key in config["hosts"]:
	host = config["hosts"][key]
	t = Thread(target=worker, args=(key, host, ))
	t.daemon = True
	t.start()
	threads.append(t)

for t in threads:
	t.join()


print(json.dumps(result))