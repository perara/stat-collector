import json
import loaders
import os
from importlib import import_module
from threading import Thread


PATH = os.path.dirname(os.path.abspath(__file__))
MODULES_PATH = PATH + "/modules/"

result = []  # All results


config = loaders.load_config()
tick = loaders.load_tick()




def worker(address, host):
	document = dict(config["global"]["base_document"])
	document["name"] = host["name"]

	# Add host address to the node
	host["address"] = address # Workaround to get address into executor without passing extra param

	# Identify all modules
	modules = [os.path.splitext(f)[0] for f in os.listdir(MODULES_PATH) if os.path.splitext(f)[1] == ".py" and f != "__init__.py"]

	# Worker function to run module
	module_threads = []
	def module_worker(module):
		mod = import_module("modules." + module)
		mod.run(host, config, document)


	for module in modules:

		# Check if module is activated in host settings
		if module in host["modules"]:
			# Use host-specific settings
			setting_enabled = host["modules"][module][0]
			setting_tick  = host["modules"][module][1]
		else:
			# Use global settings
			setting_enabled = config["global"]["modules"][module][0]
			setting_tick = config["global"]["modules"][module][1]


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


	result.append(document)




########################################
##
## Start a thread for each of the hosts
##
########################################
threads = []
for key in config["hosts"]:
	host = config["hosts"][key]
	t = Thread(target=worker, args=(key, host, ))
	t.start()
	threads.append(t)

# Wait for all tasks to finish
for thread in threads:
	thread.join()

# Increase tick count
loaders.save_tick(tick + 1)

print(json.dumps(result))