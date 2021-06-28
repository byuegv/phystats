# -*- coding:utf-8 -*-

import argparse
from phystats.logger import logger
from phystats.collector.collect import collect_metrics
from phystats.collector.k8s_collector import k8s_cluster_info
from phystats.repeat_timer import RepeatTimer
from phystats.kafkah.kafka_helper import KafkaHelper


parser = argparse.ArgumentParser()

parser.add_argument('--host', default="localhost", type=str, help="prometheus host")
parser.add_argument('--port', default="9090", type=str, help="prometheus port")
parser.add_argument('--kafka-host', default="localhost", type=str, help="kafka host")
parser.add_argument('--kafka-port', default="9092", type=str, help="kafka port")
parser.add_argument('--kafka-topic', default="phystats", type=str, help="kafka topic")

parser.add_argument('--role', default="collector", type=str, choices=["collector","consumer" "k8s_info"],
                    help="The role of current: collector to get prometheus metrics" +
                         " k8s_info to get k8s_cluster_info" +
                         " consumer to consume msgs from kafka")

args = parser.parse_args()



kafka_helper = KafkaHelper(topic=args.topic, host=args.kafka_host, port=args.kafka_port)

def get_k8s_cluster_info():
    msgs = k8s_cluster_info()
    print(len(msgs))
    for msg in msgs:
        print(msg)
    
    kafka_helper.send_msg_list(msgs, topic=None)

def get_metrics():
    msgs = collect_metrics(host=host=args.host, port=args.port)
    print(len(msgs))
    for msg in msgs:
        print(msg)

    kafka_helper.send_msg_list(msgs, topic=None)

def consume_msgs():
    kafka_helper = KafkaHelper(topic=args.topic, host=args.kafka_host, port=args.kafka_port)
    msgs = kafka_helper.consume_data(topic=None, boot_server=None, limit=None)
    print(len(msgs))


if __name__ == '__main__':
    logger.info("Main thread start!")
    # get_k8s_cluster_info()
    # get_metrics()

    if args.role == "collector":
        collect_timer = RepeatTimer(5.0, get_metrics)
        collect_timer.start()
    elif args.role == "consumer":
        consume_timer = RepeatTimer(5.0, consume_msgs)
        consume_timer.start()
    elif args.role == "k8s_info":
        k8s_timer = RepeatTimer(15.0, get_k8s_cluster_info)
        k8s_timer.start()

