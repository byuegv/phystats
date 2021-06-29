# -*- coding:utf-8 -*-

import json
import time
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import kafka_errors
from phystats.logger import logger


class KafkaHelper(object):
    """
    Kafka helper
    """
    def __init__(self, topic, host='localhost', port=9092):
        super(KafkaHelper, self).__init__()
        self.boot_server = "{}:{}".format(host, port)
        self.topic = topic

        self.producer = producer = KafkaProducer(bootstrap_servers=[self.boot_server], 
                                                 key_serializer=lambda k: json.dumps(k).encode('utf8'),
                                                 value_serializer=lambda v: json.dumps(v).encode('utf8'))
    
    def set_topic(self, topic):
        self.topic = topic
    
    def send_msg(self, msg, topic=None):
        """
        向kafka写入一条信息
        @msg:
        @topic:
        """
        if not topic:
            topic = self.topic
        try:
            logger.info("Start send data to server={}, topic={}".format(self.boot_server, topic))
            start_time = time.time()
            future = self.producer.send(topic, value=msg)
            cost_time = time.time() - start_time
            logger.info("Send one msg cost: {} s".format(cost_time))
        except Exception as e:
            logger.error("Send msg={} to kafka failed!".format(msg))
        finally:
            self.producer.flush(timeout=30)
    
    def send_msg_list(self, msg_list, topic=None):
        """
        向kafka写入多条信息
        @msg_list:
        @topic:
        """
        if not topic:
            topic = self.topic
        try:
            logger.info("Start send data to server={}, topic={}".format(self.boot_server, topic))
            start_time = time.time()
            for msg in msg_list:
                future = self.producer.send(topic, value=msg)
            cost_time = time.time() - start_time
            logger.info("Send {} messages cost: {} s".format(len(msg_list), cost_time))
        except Exception as e:
            logger.error("Send msgs_list to kafka failed!")
        finally:
            self.producer.flush(timeout=30)

    def consume_data(self, topic=None, boot_server=None, limit=None):
        """
        消费信息
        @topic:
        @boot_server:
        @limit:
        """
        if not topic:
            topic = self.topic
        if not boot_server:
            boot_server = self.boot_server
        consumer = KafkaConsumer(topic, bootstrap_servers=boot_server)
        
        logger.info("Start consume data from server={}, topic={}".format(boot_server, topic))
        msgs = []
        cur_count = 0
        for msg in consumer:
            cur_count += 1
            _msg_value = str(msg.value, encoding="utf8").replace('"', '')
            logger.debug("{} {} {}".format(msg.topic, msg.offset, _msg_value))
            msgs.append(_msg_value)
            if limit and cur_count >= limit:
                logger.info("{} messages consumed!".format(cur_count))
                break
        return msgs