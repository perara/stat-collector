from executor import execute

def run(host, config, output):
    memory_free = execute("mem_free.sh", host)
    memory_total = execute("mem_total.sh", host)
    output["memory_free"] = int(memory_free)
    output["memory_total"] = int(memory_total)
    output["memory_used"] = int(memory_total) - int(memory_free)