from executor import execute

def run(parser):
    updates_all = execute("update.sh", parser.host)
    updates = updates_all.strip().decode().split(";")
    updates_security = updates[0]
    updates_packages = updates[1]

    parser.measurement("updates")\
        .pair("type", "security")\
        .value(int(updates_security))

    parser.measurement("updates") \
        .pair("type", "packages") \
        .value(int(updates_packages))