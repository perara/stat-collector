DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPT_PATH="/../scripts/cpu.sh"
CPU_SCRIPT=$DIR$SCRIPT_PATH

ssh -p$1 $2@$3 "bash -s"< $CPU_SCRIPT
