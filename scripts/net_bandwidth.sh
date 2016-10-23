#!/bin/bash
timestamp=$(date +%s)
IF=$1

R1=`cat /tmp/sysx-bw-rx`
T1=`cat /tmp/sysx-bw-tx`
TIME=`cat /tmp/sysx-bw-time`
DT=`expr $timestamp - $TIME`
if [ "$DT" -eq "0" ]; then
    DT=1
fi

R2=`cat /sys/class/net/$1/statistics/rx_bytes`
T2=`cat /sys/class/net/$1/statistics/tx_bytes`
echo $R2 > /tmp/sysx-bw-rx
echo $T2 > /tmp/sysx-bw-tx
echo $timestamp > /tmp/sysx-bw-time
if [ -z "$R1" ]; then
    echo 0,0
    exit 0
fi
if [ -z "$T1" ]; then
    echo 0,0
    exit 0
fi
TXBPS=`expr $T2 - $T1`
RXBPS=`expr $R2 - $R1`
TXBPS=`expr $TXBPS / $DT`
RXBPS=`expr $RXBPS / $DT`

echo $TXBPS,$RXBPS
exit 0

