from executor import execute

def run(host, config, output):
    cpu_percent = execute("cpu.sh", host)
    output["cpu"] = int(cpu_percent)
