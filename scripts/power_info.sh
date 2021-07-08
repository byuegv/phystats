#!/bin/bash

declare -a hostnames
hostnames=( "phy-1-node-5" "phy-4-node5" "phy-7-node5" )

CODE_DIR="/home/kubernetes/phystats"

kafka_host="cluster-1-node-5"
kafka_port="9092"
kafka_topic="phypower"
collect_interval=15.0
daemon_action="start"

cmd_args='"ipmitool" "sdr" "elist"'
filters='"Pwr" "vattle"'


for hostname in ${hostnames[@]}
do
    echo ssh ${hostname} \
        python3 ${CODE_DIR}/phy_power_info.py \
        --daemon \
        --daemon_action=${daemon_action} \
        --kafka_host=${kafka_host} \
        --kafka_port=${kafka_port} \
        --kafka_topic=${kafka_topic} \
        --collect_interval=${collect_interval} \
        --cmd_args ${cmd_args} \
        --filters ${filters}
done
