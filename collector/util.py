# -*- coding:utf-8 -*-
from phystats.utils import get_millisecond, local_ip_address

def format_float(value, precision=6):
    """
    将数值/字符数值转换为指定精度的float字符串
    """
    return str(round(float(value), precision))


def unified_message_format(metric, obj_name, uuid, value):
    """
    统一的message输出格式
    @name: 
    @key:
    @value:
    """
    ip = local_ip_address()
    # 物理机
    if obj_name == 'ma':
        tmp = uuid
        uuid = ip
        ip = tmp
    # 虚拟机
    elif obj_name == 'vm':
        uuid = ip[:-1] + '0'
        
    timestamp = get_millisecond()
    value = format_float(value)
    return "{}:{}:{}:{}:{}:{}|{}".format(metric.rstrip("\n"), obj_name, uuid, ip, timestamp, value, timestamp)