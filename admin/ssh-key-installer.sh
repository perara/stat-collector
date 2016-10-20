if [ $# -lt 3 ]
  then
    echo "Usage: ./ssh-key-installer <port> <username> <ip-address>"
    exit
fi

if [ ! -e "~/.ssh/id_rsa" ] ; then
	echo -e  'n\y'|ssh-keygen -q -t rsa -N "" -f ~/.ssh/id_rsa | >/dev/null
	echo "Wrote SSH Keys!"
fi

cat ~/.ssh/id_rsa.pub | ssh -p $1 $2@$3 'umask 0077; mkdir -p .ssh; cat >> .ssh/authorized_keys && echo "Key copied"'
