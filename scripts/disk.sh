df -h -BM | tail -n+2 | while read fs size used rest ; do
    if [[ $used ]] ; then
        echo "$fs;$used;$size"
    fi
done
