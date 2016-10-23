import json
import loaders
import os
from parsers import Parser
from importlib import import_module
from threading import Thread

PATH = os.path.dirname(os.path.abspath(__file__))
MODULES_PATH = PATH + "/modules/"

config = loaders.load_config()
tick = loaders.load_tick()

results = []



def worker(address, host):

	parser = Parser.new()
	parser.global_set_address(address)
	parser.global_set_host(host)
	parser.global_set_timestamp() if config["reporting"]["timestamp"] == "true" else ""
	parser.global_pair("host", host["name"])

	# Identify all modules
	modules = [os.path.splitext(f)[0] for f in os.listdir(MODULES_PATH) if os.path.splitext(f)[1] == ".py" and f != "__init__.py"]

	# Worker function to run module
	module_threads = []
	def module_worker(module):
		mod = import_module("modules." + module)
		mod.run(parser)


	for module in modules:

		# Check if module is activated in host settings
		if module in host["modules"]:
			# Use host-specific settings
			setting_enabled = host["modules"][module][0]
			setting_tick  = host["modules"][module][1]
		else:
			# Use global settings
			try:
				setting_enabled = config["global"]["modules"][module][0]
				setting_tick = config["global"]["modules"][module][1]
			except:
				continue # TODO , add warning?



		# Check if module is active in global and in host settings
		if setting_enabled == "false" or ((tick % setting_tick) != 0):
			continue

		# Start thread
		thread = Thread(target=module_worker, args=(module, ))
		thread.start()
		module_threads.append(thread)


	# Wait for all module threads to complete
	for thread in module_threads:
		thread.join()


	results.append(parser.get())



########################################
##
## Start a thread for each of the hosts
##
########################################
threads = []
for key in config["hosts"]:
	host = config["hosts"][key]
	host["address"] = key
	t = Thread(target=worker, args=(key, host, ))
	t.start()
	threads.append(t)

# Wait for all tasks to finish
for thread in threads:
	thread.join()

# Increase tick count
loaders.save_tick(tick + 1)


print(json.dumps(results))