from executor import execute

def run(host, config, output):
    hostname = execute("hostname.sh", host)
    output["hostname"] = hostname.decode().strip()
