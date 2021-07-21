# -*- coding:utf-8 -*-

import time
import socket


class BaseCollector(object):
    def __init__(self, obj_name):
        self.obj_name
    
    def get_millisecond(self):
        """
        获取毫秒时间
        """
        cur_time = time.time()
        return str(round(cur_time * 1000))

    def get_local_ip(self):
        """
        获取本机IP地址
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            return ip
        except Exception as e:
            print("Get local ip address failed! Exception {}".format(e))
        finally:
            s.close()
        return "127.0.0.1"

    def collect(self):
        """
        数据采集方法
        """
        pass