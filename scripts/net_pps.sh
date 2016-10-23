#!/bin/bash
timestamp=$(date +%s)
IF=$1

R1=`cat /tmp/sysx-pps-rx`
T1=`cat /tmp/sysx-pps-tx`
TIME=`cat /tmp/sysx-pps-time`
DT=`expr $timestamp - $TIME`
if [ "$DT" -eq "0" ]; then
    DT=1
fi

R2=`cat /sys/class/net/$1/statistics/rx_packets`
T2=`cat /sys/class/net/$1/statistics/tx_packets`
echo $R2 > /tmp/sysx-pps-rx
echo $T2 > /tmp/sysx-pps-tx
echo $timestamp > /tmp/sysx-pps-time
if [ -z "$R1" ]; then
    echo 0,0
    exit 0
fi
if [ -z "$T1" ]; then
    echo 0,0
    exit 0
fi
TXPPS=`expr $T2 - $T1`
RXPPS=`expr $R2 - $R1`
TXPPS=`expr $TXPPS / $DT`
RXPPS=`expr $RXPPS / $DT`

echo $TXPPS,$RXPPS
exit 0

