
import time

from executor import execute

def run(host, config, output):
    for iface in host["interfaces"]:
        bandwidth_in_out = execute("net_usage.sh", host, params=[iface])
        bw_io = bandwidth_in_out.decode().split("\n")
        bandwidth_in = bw_io[0]
        bandwidth_out = bw_io[1]
        output["network_%s_in" % iface] = int(bandwidth_in)
        output["network_%s_out" % iface] = int(bandwidth_out)
