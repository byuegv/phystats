#!/bin/bash

declare -a hostnames

for i in {1..11}
do
    hostnames[${i}]="k8s${i}-74"
done

CODE_DIR="/home/kubernetes/phystats"

for((i=1; i<=${#hostnames[*]}; i++))
do
    h=${hostnames[$i]}
    echo ""
    echo "${h}: ssh ${h} $*"
    echo ""
    ssh ${h} "$*"
done