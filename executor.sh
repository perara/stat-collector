socket=~/.ssh/master-$3
RETURN=$(ls $socket 2>/dev/null)

if [ -z "$RETURN" ]; then
    ssh -t -o ControlPath=$socket -o ControlMaster=auto -o ControlPersist=60 -p$1 $2@$3 "bash -s"< $4 ${@:5} 2>/dev/null
    exit 0
fi

ssh -o ControlPath=$socket -p$1 $2@$3 "bash -s"< $4 ${@:5} 2>/dev/null







