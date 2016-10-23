from executor import execute

def run(parser):
    hostname = execute("hostname.sh", parser.host)

    parser.measurement("hostname").value(hostname.decode().strip())
