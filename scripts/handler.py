#!/bin/bash

declare -a hostnames

index=1
for cluster in {1..9}
do
    for node in {1..7}
    do
        if [ ${node} -eq 1 ]; then
            hostnames[${index}]="cluster-${cluster}-master-${node}"
        else
            hostnames[${index}]="cluster-${cluster}-node-${node}"
        fi
        index=$((index + 1))
    done
done

CODE_DIR="/home/kubernetes/phystats"

for((i=1; i<=${#hostnames[*]}; i++))
do
    h=${hostnames[$i]}
    echo ""
    echo "${h}: ssh ${h} $*"
    echo ""
    # ssh ${h} "$*"
done