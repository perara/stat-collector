
import time

from executor import execute

def run(parser):
    for iface in parser.host["interfaces"]:
        bw_io = execute("net_bandwidth.sh", parser.host, params=[iface])
        bw_io = bw_io.decode().strip().split(",")

        if len(bw_io) == 2:
            parser.measurement("network")\
                .pair("device", iface)\
                .pair("type", "bandwidth")\
                .pair("direction", "out")\
                .value(int(bw_io[0]))
            parser.measurement("network") \
                .pair("device", iface) \
                .pair("type", "bandwidth") \
                .pair("direction", "in") \
                .value(int(bw_io[1]))

        pps_io = execute("net_pps.sh", parser.host, params=[iface])
        pps_io = pps_io.decode().split(",")

        if len(pps_io) == 2:
            parser.measurement("network") \
                .pair("device", iface) \
                .pair("type", "pps") \
                .pair("direction", "out") \
                .value(int(pps_io[0]))
            parser.measurement("network") \
                .pair("device", iface) \
                .pair("type", "pps") \
                .pair("direction", "in") \
                .value(int(pps_io[1]))