value=$(/usr/lib/update-notifier/apt-check 2>&1)

if [[ $value == *"apt-check"* ]]; then
   echo "-1;-1"
   exit 0
fi

echo "$value"
