#!/bin/bash

declare -a hostnames

CODE_DIR="/home/kubernetes/phystats"


host="localhost"
port="9090"
kafka_host="cluster-1-node-4"
kafka_port="9092"
kafka_topic="phystats"
collect_interval=5.0
consume_interval=5.0
k8s_interval=5.0
limit=100000
role="collector"
daemon_action="start"


cluster=${1}
if [ ! -n "${cluster}" ]; then
    echo "Please provide cluster id"
    exit 1
fi

index=1
for node in {1..7}
do
    if [ ${node} -eq 1 ]; then
        hostname="cluster-${cluster}-master-${node}"
	export PYTHONPATH=/home/kubernetes && \
        ssh ${hostname} \
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
            --role "k8s_info ${role}"

    else
        hostname="cluster-${cluster}-node-${node}"
	export PYTHONPATH=/home/kubernetes && \
        ssh ${hostname} \
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
            --role ${role}
    fi
    index=$((index + 1))
done
