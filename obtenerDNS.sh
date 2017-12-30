#!/bin/bash
sed 's/HostName//g' ./dns_publicos.txt > ok.txt
variable=`head -1 ok.txt`
export DNS_D=`echo $variable`
sed "1d" ok.txt > ok1.txt
variable1=`head -1 ok1.txt`
export DNS_B=`echo $variable1`
sed "1d" ok1.txt > ok2.txt
variable2=`head -1 ok2.txt`
export DNS_R=`echo $variable2`
rm -rf ok*.txt
exec $SHELL
