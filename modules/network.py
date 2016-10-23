
import time

from executor import execute

def run(parser):
    for iface in parser.host["interfaces"]:
        bandwidth_in_out = execute("net_usage.sh", parser.host, params=[iface])
        bw_io = bandwidth_in_out.decode().split("\n")
        bandwidth_in = bw_io[0]
        bandwidth_out = bw_io[1]

        parser.measurement("network")\
            .pair("device", iface)\
            .pair("direction", "in")\
            .value(int(bandwidth_in))
        parser.measurement("network")\
            .pair("device", iface)\
            .pair("direction", "out")\
            .value(int(bandwidth_out))