
from executor import execute

def run(host, config, output):
    disk_data = execute("disk.sh", host)
    for disk in disk_data.decode().split("\n"):
        splt = disk.split(";")

        if len(splt) is not 3:
            continue

        disk_name = splt[0]
        disk_used = int(splt[1].replace("M",""))
        disk_total = int(splt[2].replace("M",""))
        disk_small_name = disk_name.split("/").pop()

        if "tmpfs" in disk_name or "udev" in disk_name:
            continue

        output["disk_%s_used" % disk_small_name] = disk_used
        output["disk_%s_total" % disk_small_name] = disk_total
