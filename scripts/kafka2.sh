#!/bin/bash

declare -a hostnames
hostnames=( "cluster-1-node-5" "cluster-4-node5" "cluster-7-node5" )

CODE_DIR="/home/kubernetes/phystats"

from_host="localhost"
from_port="9092"
from_topic="phystats"
to_host="localhost"
to_port="9092"
to_topic="phystats"
daemon_action="start"


for hostname in ${hostnames[@]}
do
    echo ssh ${hostname} \
        python3 ${CODE_DIR}/kafka2kafka.py \
        --daemon \
        --daemon_action=${daemon_action} \
        --from_host=${from_host} \
        --from_port=${from_port} \
        --from_topic=${from_topic} \
        --to_host=${to_host} \
        --to_port=${to_port} \
        --to_topic=${to_topic}
done