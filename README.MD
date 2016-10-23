# sysx-monitor

Current features

 * CPU (Current)
 * Memory (Total/Free/Used)
 * Available Updates (Packages/Security)
 * Disk (Total/Free/Used)
 * Hostname
 * Network (PPS/Bandwidth)

### Adding a host
```bash
python3 add-host.py
```

### Run collection
Collection is ran once per execution of the collecor.py script. It collect one time unit of data for all hosts defined in the config.json file-
```bash
python3 collector.py
```

When collector.py has completed its execution, a json string will be outputted in std:out which can be appended to your log backend

### Example output: JSON
```json
[{
	"disk_sda1_total": 472,
	"cpu": 0,
	"memory_total": 8173468,
	"updates_security": 0,
	"host": "database",
	"updates_packages": 0,
	"full_message": "",
	"timestamp": 1476992969,
	"disk_database--vg-root_total": 71958,
	"short_message": "sysx.reporter.linux",
	"memory_used": 1712752,
	"network_ens18_out": 0,
	"network_ens18_in": 0,
	"disk_sda1_used": 198,
	"memory_free": 6460716,
	"version": "1.1",
	"level": 1,
	"disk_database--vg-root_used": 20003
}]
```
### Example output: InfluxDB
```
disk,device=sda1,host=database,type=used value=198 1477232909166764032
disk,device=sda1,host=database,type=total value=472 1477232909166764032
disk,device=sda1,host=database,type=free value=274 1477232909166764032
network,device=ens18,direction=out,type=bandwidth,host=database value=4190 1477232909166764032
network,device=ens18,direction=in,type=bandwidth,host=database value=4721 1477232909166764032
memory,host=database,type=free value=5864456 1477232909166764032
memory,host=database,type=total value=8173468 1477232909166764032
memory,host=database,type=used value=2309012 1477232909166764032
network,device=ens18,direction=out,type=pps,host=database value=36 1477232909166764032
network,device=ens18,direction=in,type=pps,host=database value=35 1477232909166764032
hostname,host=database value="database" 1477232909166764032
cpu,host=database value=7 1477232909166764032
updates,host=database,type=security value=5 1477232909166764032
```

## Configuration
In the configuration file config.json, you can set host specific options and define which backend you wish sysx-monitor to use
when running run.py

### Reporting configuration
```
  "reporting": {
    "mode": "http",
    "url": "10.0.1.15",
    "port": 8086,
    "prefix": "/write?db=sysx-monitor",
    "engine": "influxdb",
    "timestamp": "true"
  }
```
Currently, two backends are supported *influxdb* and *elasticsearch*. The timestamp property sets the timestamp globally on the document if set to true. This is useful for especially influxdb.

mode determines which protocol to use in run.py. only *http* is supported at the moment
The prefix property defines in influxdb which database to connect to, while in elasticsearch/graylog, one would enter /gelf here.

### Modules
Moddules are defined in the configuration file where all global modules (those which should run on all hosts) are under the "global" property.

Each of the properties have an array which determine if its active and how frequently the module should run:
```
"cpu": ["true", 1] 
```
This means that the "cpu" module is activated and should every *tick*, Which is evertime you run collector.py.

```
"cpu": ["true", 3] 
```
Now the cpu module runs every third tick.

### Host specific modules
Hosts can also have specific modules, for-example:
```
"hosts": {
    "10.0.1.15": {
      "name": "database",
      "modules": {
	"very_specific_module": ["true", 1]
      }
    }
}
```
This *very_specific_module* are added to the modules directory with its corresponding bash script in /scripts.
The behaviour of the tick / enabling are the same as for global modules.

Also host specific overrides can be done, lets say you disable *cpu* globally, you can then reenable cpu for only a specific host.

### Creating a Module
1. Create a python file in /modules, for example cpu.py
2. All modules must use following skeleton:
```python
from executor import execute
def run(parser):
    pass
```
3. Create your bash script. This script must return the value of your computation in std:out
4. Add this script to /scripts. In our example /scripts/cpu.sh:
```bash
echo $[100-$(vmstat 1 2|tail -1|awk '{print $15}')]
```
5. Create your python manipulation logic:
```python
from executor import execute
def run(parser):
    cpu_percent = execute("cpu.sh", parser.host)
    parser.measurement("cpu").value(int(cpu_percent))
```
6. Now your module should be working :)


## Parser API
The parser api are a self referencing API which allows for chaining, As a reference i recommend taking a look at existing modules
```python
    parser.measurement("disk").pair("device", disk_small_name).pair("type", "used").value(disk_used)
    parser.measurement("disk").pair("device", disk_small_name).pair("type", "total").value(disk_total)
    parser.measurement("disk").pair("device", disk_small_name).pair("type", "free").value(disk_free)
```
