from executor import execute


def run(parser):
    cpu_percent = execute("cpu.sh", parser.host)
    parser.measurement("cpu").value(int(cpu_percent))