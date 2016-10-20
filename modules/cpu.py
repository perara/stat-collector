from executor import execute

def run(host, config, output):
    hostname = execute("hostname.sh", host)
    output["host"] = hostname.decode().strip()
