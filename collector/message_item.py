# -*- coding:utf-8 -*-

class MessageItem(object):
    """
    统一定义消息格式
    """
    def __init__(self, metric, obj_name, ip, id, timestamp, value):
        self.metric = metric
        self.obj_name = obj_name
        self.ip = ip
        self.id = id
        self.timestamp = timestamp
        self.value = value
    
    def __str__(self):
        return f"{self.metric}:{self.obj_name}:{self.ip}:{self.id}:{self.timestamp}:{self.value}|{self.timestamp}"
