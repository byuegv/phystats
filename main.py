# -*- coding:utf-8 -*-

from phystats.logger import logger
from phystats.collector.collect import collect_metrics
from phystats.collector.k8s_collector import k8s_cluster_info
from phystats.repeat_timer import RepeatTimer
from phystats.kafkah.kafka_helper import KafkaHelper


kafka_helper = KafkaHelper(topic="phystats", host='localhost', port=9092)

def get_k8s_cluster_info():
    msgs = k8s_cluster_info()
    print(len(msgs))
    for msg in msgs:
        print(msg)
    
    kafka_helper.send_msg_list(msgs, topic=None)

def get_metrics():
    msgs = collect_metrics(host='localhost', port=9090)
    print(len(msgs))
    for msg in msgs:
        print(msg)

    kafka_helper.send_msg_list(msgs, topic=None)

def consume_msgs():
    kafka_helper = KafkaHelper(topic="phystats", host='localhost', port=9092)
    msgs = kafka_helper.consume_data(topic=None, boot_server=None, limit=None)
    print(len(msgs))


if __name__ == '__main__':
    logger.info("Main thread start!")
    # get_k8s_cluster_info()
    # get_metrics()
    
    collect_timer = RepeatTimer(5.0, get_metrics)
    consume_timer = RepeatTimer(5.0, consume_msgs)

    collect_timer.start()
    consume_timer.start()

