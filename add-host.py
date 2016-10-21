import subprocess
import os
import sys
import json


print("We will now begin to configure a remote host for polling support")
print("The remote host will install the public key of the master server")
print("This is to easily connect and retrieve information about the client")
print("First connection is a username/password authentication")


try:
    input = raw_input
except NameError:
    pass

PATH = os.path.dirname(os.path.realpath(__file__))
ssh_install_script = os.path.join(PATH, "admin/ssh-key-installer.sh")
config_file = os.path.join(PATH, "config.json")

# Load configuration
with open(config_file) as data_file:
    config = json.load(data_file)

# Input host
host = input("Host: ")

if host in config["hosts"]:
    print("Host %s is allready installed according to the hosts list" % host)
    yn = input("Remove entry?: ")
    if yn is "y" or yn is "Y":
        with open(config_file, 'w') as outfile:
            del config["hosts"][host]
            json.dump(config, outfile, indent=4, sort_keys=True)
        print("Removed entry, run script again to install host!")
        exit(0)
    else:
        print("Nothing to do... Exiting.")
        exit(0)

# Username and port
username = input("Username: ")
port = input("Port: ")

cmd = ['/bin/bash', ssh_install_script]
cmd.extend([port, username, host])
subprocess.call(cmd)

print("Done! Now confirming that keys were added successfully.")
print("Attempting to poll for CPU usage: ")

try:
    script = os.path.join(PATH, "scripts/cpu.sh")
    cmd2 = ['/bin/bash', os.path.join(PATH, "admin/test-ssh.sh"), port, username, host]
    output = subprocess.check_output(cmd2)
    output = output.strip()
    output = int(output)
except:
    print("Unexpected error:", sys.exc_info()[0])
    exit(0)

print("Receieved %s CPU from %s" % (output, host))
print("Successfully tested host")

nics = input("List all network interfaces of the remote host as a comma-separated list(ie: eth0,eth1): ")
nics = nics.split(",")

name = input("Name of host: ")

print("Writing host entry in config file...")
config["hosts"][host] = {
    "name": name,
    "port": port,
    "username": username,
    "protocol": "ssh",
    "modules": {},
    "interfaces": nics

}

print("Saving config file!")
# Saving json
with open(config_file, 'w') as outfile:
    json.dump(config, outfile, indent=4, sort_keys=True)
print("Done. Exiting...")

exit(0)
