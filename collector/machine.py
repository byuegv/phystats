# -*- coding:utf-8 -*-

import time
from phystats.collector.util import unified_message_format
from phystats.collector import config
from phystats.logger import logger
from phystats.utils import query_prometheus_data

def collect_ma(host='localhost', port=9090):
    """
    物理机机指标信息
    """
    msgs = []
    names = config.ma_names
    pqls = config.ma_pqls
    logger.info("Collect ma metrics ...")
    obj_name = "ma"
    uuid = os.getenv("CLUSTER_ID", "cluster-1")
    for pql, name in zip(pqls, names):
        response = query_prometheus_data(pql, host=host, port=port)
        if response:
            for data in response['data']['result']:
                metric = name
                value = data['value'][1]
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
        ma_msgs = collect_ma(host, port)
        msgs.extend(ma_msgs)
    except Exception as e:
        logger.info("Encounter exception when collecting metrics, Exception: {}".format(e))

    cost_time = time.time() - start_time
    logger.info("Collect all metrics cost: {} s".format(cost_time))
    
    return msgs