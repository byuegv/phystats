# -*- coding:utf-8 -*-
import time
import socket
import requests
from phystats.logger import logger

def get_millisecond():
    """
    获取毫秒时间
    """
    cur_time = time.time()
    return str(round(cur_time * 1000))


def local_ip_address():
    """
    获取本机IP地址
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        return ip
    except Exception as e:
        logger.info("Get local ip address failed! Exception {}".format(e))
    finally:
        s.close()


def query_prometheus_data(pql, host='localhost', port=9090, params=None, data=None):
    """
    从prometheus查询指标数据
    @pql: promQL
    @host:
    @port:
    @params:
    @data:
    """
    url = "http://{}:{}/api/v1/query?query={}".format(host, port, pql)
    try:
        logger.info("Request: {}".format(url))
        response = requests.get(url)
        result = response.json()
        logger.info("Response: {}; Result: {}".format(response, result))
        return result
    except Exception as e:
        logger.error("Get metrics failed from prometheus! Exception: {}".format(e))