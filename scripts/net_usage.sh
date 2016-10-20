#!/bin/bash

_die() {
    printf '%s\n' "$@"
    exit 1
}

_interface=$1

[[ ${_interface} ]] || _die 'Usage: ifspeed [interface]'
grep -q "^ *${_interface}:" /proc/net/dev || _die "Interface ${_interface} not found in /proc/net/dev"

_interface_bytes_in_old=$(awk "/^ *${_interface}:/"' { if ($1 ~ /.*:[0-9][0-9]*/) { sub(/^.*:/, "") ; print $1 } else { print $2 } }' /proc/net/dev)
_interface_bytes_out_old=$(awk "/^ *${_interface}:/"' { if ($1 ~ /.*:[0-9][0-9]*/) { print $9 } else { print $10 } }' /proc/net/dev)

sleep 1

_interface_bytes_in_new=$(awk "/^ *${_interface}:/"' { if ($1 ~ /.*:[0-9][0-9]*/) { sub(/^.*:/, "") ; print $1 } else { print $2 } }' /proc/net/dev)
_interface_bytes_out_new=$(awk "/^ *${_interface}:/"' { if ($1 ~ /.*:[0-9][0-9]*/) { print $9 } else { print $10 } }' /proc/net/dev)

    printf '%s%s\n' ''  "$(( _interface_bytes_in_new - _interface_bytes_in_old ))" \
                      '' "$(( _interface_bytes_out_new - _interface_bytes_out_old ))"

    _interface_bytes_in_old=${_interface_bytes_in_new}
    _interface_bytes_out_old=${_interface_bytes_out_new}
