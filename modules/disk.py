
from executor import execute

def run(parser):
    disk_data = execute("disk.sh", parser.host)
    for disk in disk_data.decode().split("\n"):
        splt = disk.split(";")

        if len(splt) is not 3:
            continue

        disk_name = splt[0]
        disk_used = int(splt[1].replace("M",""))
        disk_total = int(splt[2].replace("M",""))
        disk_free = disk_total - disk_used
        disk_small_name = disk_name.split("/").pop()

        if "tmpfs" in disk_name or "udev" in disk_name:
            continue

        # Some virtual disks have hostname-- as prefix. remove this
        if "--" in disk_small_name:
            disk_small_name = disk_small_name.split("--")[1]


        parser.measurement("disk").pair("device", disk_small_name).pair("type", "used").value(disk_used)
        parser.measurement("disk").pair("device", disk_small_name).pair("type", "total").value(disk_total)
        parser.measurement("disk").pair("device", disk_small_name).pair("type", "free").value(disk_free)
