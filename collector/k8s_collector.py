# -*- coding:utf-8 -*-

import time
from phystats.utils import local_ip_address, get_millisecond
from phystats.logger import logger
from kubernetes import client, config


def cpu_format_to_float(cpu_data):
    cpu_string = cpu_data[:-1]
    return float(cpu_string)


def float_to_cpu_format(float_data):
    return str(float_data) + "m"


def mem_format_to_float(mem_data):
    mem_string = mem_data[:-2]
    return float(mem_string)


def float_to_mem_format(float_data):
    return str(float_data) + "Mi"


def unified_msg_format(key, name, ip, value):
    """
    统一的message输出格式
    @ip:
    @name: 
    @key:
    @value:
    """
    millisecond = get_millisecond()
    return "{}:{}:{}:{}:{}|{}".format(key, name, ip, millisecond, value, millisecond)

def k8s_cluster_info():
    """
    获取k8s集群信息
    """
    config.load_kube_config()

    v1 = client.CoreV1Api()

    logger.info("Get k8s info start")

    ret = v1.list_pod_for_all_namespaces(watch=False)

    logger.info("k8s information: {}".format(ret))

    labels = ["cluster_name"]
    resource_name = ["cpu", "memory"]
    msgs = []
    for item in ret.items:
        limit_cpu = 0
        limit_mem = 0
        request_cpu = 0
        request_mem = 0
        request_es = 0

        ip = None
        if item.status.host_ip:
            ip = item.status.host_ip
        else:
            ip = local_ip_address()

        if item.metadata.cluster_name:
            msgs.append(unified_msg_format("clu_na", item.metadata.name, ip, item.metadata.cluster_name))
        else:
            msgs.append(unified_msg_format("clu_na", item.metadata.name, ip, "None"))

        for c in item.spec.containers:
            resource = c.resources
            limits = resource.limits
            requests = resource.requests
            if limits:
                if 'cpu' in limits:
                    try:
                        limit_cpu = limit_cpu + cpu_format_to_float(limits['cpu'])
                    except Exception as e:
                        limit_cpu = 0
                if 'memory' in limits:
                    try:
                        limit_mem = limit_mem + mem_format_to_float(limits['memory'])
                    except Exception as e:
                        limit_mem = 0  
            if requests:
                if 'cpu' in requests:
                    try:
                        request_cpu = request_cpu + cpu_format_to_float(requests['cpu'])
                    except Exception as e:
                        request_cpu = 0  
                if 'memory' in requests:
                    try:
                        request_mem = request_mem + mem_format_to_float(requests['memory'])
                    except Exception as e:
                        request_mem = 0  
                if 'ephemeral-storage' in requests:
                    try:
                        request_es = request_es + mem_format_to_float(requests['ephemeral-storage'])
                    except Exception as e:
                        request_es = 0 

        msgs.append(unified_msg_format("cpu_re", item.metadata.name, ip, float_to_cpu_format(request_cpu)))
        msgs.append(unified_msg_format("mem_re", item.metadata.name, ip, float_to_mem_format(request_mem)))
        msgs.append(unified_msg_format("cpu_li", item.metadata.name, ip, float_to_cpu_format(limit_cpu)))
        msgs.append(unified_msg_format("mem_li", item.metadata.name, ip, float_to_mem_format(limit_mem)))
        msgs.append(unified_msg_format("es_re", item.metadata.name, ip, float_to_mem_format(request_es)))
    return msgs