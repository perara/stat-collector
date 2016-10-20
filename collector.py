import json
from config import config
import time
import subprocess
import os
PATH = os.path.dirname(os.path.abspath(__file__))
SCRIPT_PATH = PATH + "/scripts/"


def execute_script(script_file):
    command = "/bin/bash " +  SCRIPT_PATH + script_file
    output = subprocess.check_output(command.split())
    return output.strip()


output = {
	"version": "1.1",
	"host": "dev.grm.sysx.lan",
	"short_message": "sysx.reporter.linux",
	"full_message": "",
	"timestamp": int(time.time()),
	"level": 1

}

if config["modules"]["cpu"]:
	cpu_percent = execute_script("cpu.sh")
	output["cpu"] = int(cpu_percent)

if config["modules"]["memory"]:
	memory_free = execute_script("mem_free.sh")
	memory_total = execute_script("mem_total.sh")
	output["memory_free"] = int(memory_free)
	output["memory_total"] = int(memory_total)
	output["memory_used"] = int(memory_total) - int(memory_free)

if config["modules"]["network"]:
	for iface in config["network"]["interfaces"]:
		bandwidth_in_out = execute_script("net_usage.sh %s" % iface)
		bandwidth_in = bandwidth_in_out.split("\n")[0]
		bandwidth_out = bandwidth_in_out.split("\n")[1]
		output["network_%s_in" % iface] = int(bandwidth_in)
		output["network_%s_out" % iface] = int(bandwidth_out)

if config["modules"]["updates"]:
	updates_all = execute_script("update.sh")
	updates_security = updates_all.split(";")[0]
	updates_packages = updates_all.split(";")[1]
	output["updates_security"] = int(updates_security)
	output["updates_packages"] = int(updates_packages)

if config["modules"]["disk"]:
	disk_data = execute_script("disk.sh")
	for disk in disk_data.split("\n"):
		splt = disk.split(";")
		disk_name = splt[0]
		disk_used = int(splt[1].replace("M",""))
		disk_total = int(splt[2].replace("M",""))
		disk_small_name = disk_name.split("/").pop()

		if "tmpfs" in disk_name or "udev" in disk_name:
			continue

		output["disk_%s_used" % disk_small_name] = disk_used
		output["disk_%s_total" % disk_small_name] = disk_total

print(json.dumps(output))
