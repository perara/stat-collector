from executor import execute

def run(parser):
    memory_free = execute("mem_free.sh", parser.host)
    memory_total = execute("mem_total.sh", parser.host)

    parser.measurement("memory").pair("type", "free").value(int(memory_free))
    parser.measurement("memory").pair("type", "total").value(int(memory_total))
    parser.measurement("memory").pair("type", "used").value(int(memory_total) - int(memory_free))