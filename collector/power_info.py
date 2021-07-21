# -*- coding:utf-8 -*-

import os
import subprocess
from phystats.collector.util import unified_message_format
from phystats.logger import logger


def power_info(cmd_args, filters):
    """
    获取物理机能耗数据
    """
    origin_data = None
    try:
        logger.debug("exec {}".format(",".join(cmd_args)))
        origin_data = subprocess.check_output(cmd_args).decode('utf-8')
        logger.debug("Origin_data: {}".format(origin_data))
    except Exception as e:
        logger.info("Get origin data failed! Exception: {}".format(e))
    
    origin_data = origin_data.split('\n')

    # 提取原始相关数据
    raw_lists = []
    for i in range(len(origin_data)):
        s = origin_data[i]
        if(len(s) < 4):
            continue
        item = list(map(lambda x: x.strip().replace(' ','-'), s.split('|')))
        raw_lists.append(item)
    
    # 过滤非能耗数据
    filtered_data = []
    for item in raw_lists:
        for f in filters:
            if f in item[0]:
                filtered_data.append(item)
                break
    
    msgs = []
    obj_name = 'ma'
    uuid = os.getenv("CLUSTER_ID", "cluster-1")
    for item in filtered_data:
        try:
            metric = item[0]
            value = '0'
            if len(item) >= 5 and len(item[4]) > 0:
                value = item[4].split('-')[0].strip()
            value = float(value)
            msg = unified_message_format(metric, obj_name, uuid, value)
            msgs.append(msg)
        except Exception as e:
            logger.debug("Convert data failed: Exception: {}".format(e))
    return msgs

