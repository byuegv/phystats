# -*- coding:utf-8 -*-
from phystats.utils import get_millisecond, local_ip_address

def format_float(value, precision=6):
    """
    将数值/字符数值转换为指定精度的float字符串
    """
    return str(round(float(value), precision))


def unified_message_format(name, key, value):
    """
    统一的message输出格式
    @name: 
    @key:
    @value:
    """
    ip = local_ip_address()
    millisecond = get_millisecond()
    value = format_float(value)
    return "{}:{}:{}:{}:{}".format(name.rstrip("\n"), key, ip, millisecond, value)