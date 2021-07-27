# -*- coding:utf-8 -*-

import os
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

    obj_name = "ctr"

    for pql, name in zip(pqls, names):
        response = query_prometheus_data(pql, host=host, port=port)
        if response:
            for data in response['data']['result']:
                metric = name
                value = data['value'][1]
                uuid = data['metric']['name']
                msg = unified_message_format(metric, obj_name, uuid, value)
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

    obj_name = "ctr"

    for pql, name in zip(pqls, names):
        response = query_prometheus_data(pql, host=host, port=port)
        if response:
            for data in response['data']['result']:
                metric = name
                uuid = pql
                value = data['value'][1]
                msg = unified_message_format(metric, obj_name, uuid, value)
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

    obj_name = "vm"
    uuid = os.getenv("MACHINE_ADDRESS", "")

    for pql, name in zip(pqls, names):
        response = query_prometheus_data(pql, host=host, port=port)
        if response:
            for data in response['data']['result']:
                metric = name
                #uuid = data['metric']['pdu_id']
                value = data['value'][1]
                msg = unified_message_format(metric, obj_name, uuid, value)
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
    obj_name = "pd"

    for pql, name in zip(pqls, names):
        response = query_prometheus_data(pql, host=host, port=port)
        if response:
            for data in response['data']['result']:
                metric = name
                uuid = data['metric']['container_label_io_kubernetes_pod_name'] 
                value = data['value'][1]
                msg = unified_message_format(metric, obj_name, uuid, value)
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
    obj_name = "vm"
    uuid = os.getenv("MACHINE_ADDRESS", "")
    for pql, name in zip(pqls, names):
        response = query_prometheus_data(pql, host=host, port=port)
        if response:
            for data in response['data']['result']:
                metric = name
                value = data['value'][1]
                # uuid = pql
                msg = unified_message_format(metric, obj_name, uuid, value)
                msgs.append(msg)
    return msgs


def collect_metrics(host='localhost', port=9090):
    """
    获取所有指标信息
    """
    msgs = []
    start_time = time.time()

    try:
        container_msgs = collect_container(host, port)
        msgs.extend(container_msgs)
    except Exception as e:
        logger.info("Encounter exception when collecting metrics, Exception: {}".format(e))

    
    try:
        dif_format_msgs = collect_dif_format(host, port)
        msgs.extend(dif_format_msgs)
    except Exception as e:
        logger.info("Encounter exception when collecting metrics, Exception: {}".format(e))

    try:
        pdu_msgs = collect_pdu(host, port)
        msgs.extend(pdu_msgs)
    except Exception as e:
        logger.info("Encounter exception when collecting metrics, Exception: {}".format(e))
    
    try:
        pod_msgs = collect_pod(host, port)
        msgs.extend(pod_msgs)
    except Exception as e:
        logger.info("Encounter exception when collecting metrics, Exception: {}".format(e))

    try:
        vm_msgs = collect_vm(host, port)
        msgs.extend(vm_msgs)
    except Exception as e:
        logger.info("Encounter exception when collecting metrics, Exception: {}".format(e))

    cost_time = time.time() - start_time
    logger.info("Collect all metrics cost: {} s".format(cost_time))
    
    return msgs