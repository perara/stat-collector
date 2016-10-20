from executor import execute

def run(host, config, output):
    updates_all = execute("update.sh", host)
    updates = updates_all.strip().decode().split(";")
    updates_security = updates[0]
    updates_packages = updates[1]
    output["updates_security"] = int(updates_security)
    output["updates_packages"] = int(updates_packages)