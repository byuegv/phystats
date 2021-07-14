#!/bin/bash

declare -a hostnames
hostnames=( "cluster-1-node-5" "cluster-4-node5" "cluster-7-node5" )

CODE_DIR="/home/kubernetes/phystats"

from_host="localhost"
from_port="9092"
from_topic="phystats"
file_prefix="/data/vm-con"
limit=1000000
daemon_action="start"


        python3 ${CODE_DIR}/datasave.py \
        --daemon \
        --daemon_action=${daemon_action} \
        --from_host=${from_host} \
        --from_port=${from_port} \
        --from_topic=${from_topic} \
        --file_prefix=${file_prefix} \
        --limit=${limit}
