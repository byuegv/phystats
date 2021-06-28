# -*- coding:utf-8 -*-

import time
from phystats.collector.util import unified_message_format
from phystats.collector import config
from phystats.logger import logger
from phystats.utils import query_prometheus_data


def collect_container(host='localhost', port=9090):
    """
    container 指标信息
    """
    msgs = []
    names = config.container_names
    pqls = config.container_pqls
    logger.info("Collect container metrics ...")
    for pql, name in zip(pqls, names):
        response = query_prometheus_data(pql, host=host, port=port)
        if response:
            for data in response['data']['result']:
                key = data['metric']['name']
                value = data['value'][1]
                msg = unified_message_format(name=name, key=key, value=value)
                msgs.append(msg)
    return msgs

def collect_dif_format(host='localhost', port=9090):
    """
    container dif format 指标信息
    """
    msgs = []
    names = config.dif_format_names
    pqls = config.dif_format_pqls
    logger.info("Collect container dif format metrics ...")
    for pql, name in zip(pqls, names):
        response = query_prometheus_data(pql, host=host, port=port)
        if response:
            for data in response['data']['result']:
                key = "ct"
                value = data['value'][1]
                msg = unified_message_format(name=name, key=key, value=value)
                msgs.append(msg)
    return msgs


def collect_pdu(host='localhost', port=9090):
    """
    container dif format 指标信息
    """
    msgs = []
    names = config.pdu_names
    pqls = config.pdu_pqls
    logger.info("Collect pdu metrics ...")
    for pql, name in zip(pqls, names):
        response = query_prometheus_data(pql, host=host, port=port)
        if response:
            for data in response['data']['result']:
                key = data['metric']['pdu_id']
                value = data['value'][1]
                msg = unified_message_format(name=name, key=key, value=value)
                msgs.append(msg)
    return msgs

def collect_pod(host='localhost', port=9090):
    """
    k8s pod 指标信息
    """
    msgs = []
    names = config.pod_names
    pqls = config.pod_pqls
    logger.info("Collect pod metrics ...")
    for pql, name in zip(pqls, names):
        response = query_prometheus_data(pql, host=host, port=port)
        if response:
            for data in response['data']['result']:
                key = data['metric']['container_label_io_kubernetes_pod_name'] 
                value = data['value'][1]
                msg = unified_message_format(name=name, key=key, value=value)
                msgs.append(msg)
    return msgs

def collect_vm(host='localhost', port=9090):
    """
    虚拟机指标信息
    """
    msgs = []
    names = config.vm_names
    pqls = config.vm_pqls
    logger.info("Collect vm metrics ...")
    for pql, name in zip(pqls, names):
        response = query_prometheus_data(pql, host=host, port=port)
        if response:
            for data in response['data']['result']:
                key = "vm"
                value = data['value'][1]
                msg = unified_message_format(name=name, key=key, value=value)
                msgs.append(msg)
    return msgs


def collect_metrics(host='localhost', port=9090):
    """
    获取所有指标信息
    """
    msgs = []
    start_time = time.time()

    container_msgs = collect_container(host, port)
    dif_format_msgs = collect_dif_format(host, port)
    pdu_msgs = collect_pdu(host, port)
    pod_msgs = collect_pod(host, port)
    vm_msgs = collect_vm(host, port)

    msgs.extend(container_msgs)
    msgs.extend(dif_format_msgs)
    msgs.extend(pdu_msgs)
    msgs.extend(pod_msgs)
    msgs.extend(vm_msgs)

    cost_time = time.time() - start_time
    logger.info("Collect all metrics cost: {} s".format(cost_time))
    
    return msgs