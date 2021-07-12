#!/bin/bash

declare -a hostnames

CODE_DIR="/home/kubernetes/phystats"


host="localhost"
port="9090"
kafka_host="data-center-3"
kafka_port="9092"
kafka_topic="phystats"
collect_interval=5.0
consume_interval=5.0
k8s_interval=5.0
limit=100000
role="collector"
daemon_action="stop"

            python3 ${CODE_DIR}/main.py \
            --daemon \
            --daemon_action=${daemon_action} \
            --host=${host} \
            --port=${port} \
            --kafka_host=${kafka_host} \
            --kafka_port=${kafka_port} \
            --kafka_topic=${kafka_topic} \
            --collect_interval=${collect_interval} \
            --consume_interval=${consume_interval} \
            --k8s_interval=${k8s_interval} \
            --limit=${limit} \
            --role "k8s_info" ${role}
