# sysx-monitor

Current features

 * CPU
 * Memory
 * Updates Available
 * Disk Usage
 * Hostname
 * Network

### Adding a host
```bash
python3 add-host.py
```

### Run collection
Collection is ran once per execution of the collecor.py script. It collect one time unit of data for all hosts defined in the config.json file-
```bash
python3 collector.py
```

### Example output
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