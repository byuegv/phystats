# -*- coding:utf-8 -*-

import argparse
import json
import time
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import kafka_errors
from phystats.logger import logger


parser = argparse.ArgumentParser()

parser.add_argument('--from_host', default="localhost", type=str, help="host of source kafka")
parser.add_argument('--from_port', default="9092", type=str, help="port of source kafka")
parser.add_argument('--from_topic', default="phystats", type=str, help="topic of source kafka")
parser.add_argument('--to_host', default="localhost", type=str, help="host of to kafka")
parser.add_argument('--to_port', default="9092", type=str, help="port of to kafka")
parser.add_argument('--to_topic', default="phystats", type=str, help="topic of to kafka")

args = parser.parse_args()


def kafka_to_kafka(from_server, from_topic, to_server, to_topic):
    consumer = KafkaConsumer(from_topic, bootstrap_servers=from_server)
    
    producer = producer = KafkaProducer(bootstrap_servers=[to_server], 
                                        key_serializer=lambda k: json.dumps(k).encode('utf8'),
                                        value_serializer=lambda v: json.dumps(v).encode('utf8'))
        
    logger.info("Start consume data from server={}, topic={}".format(from_server, from_topic))
    cur_count = 0
    for msg in consumer:
        cur_count += 1
        _msg_value = str(msg.value, encoding="utf8").replace('"', '')
        logger.debug("{} {} {}".format(msg.topic, msg.offset, _msg_value))
        try:
            logger.debug("Start send data to server={}, topic={}".format(to_server, to_topic))
            future = producer.send(to_topic, value=_msg_value)
        except Exception as e:
            logger.error("Send msg={} to kafka {} failed!".format(_msg_value, to_server))


if __name__ == '__main__':
    logger.info("Main thread start!")
    for k in list(vars(args).keys()):
        logger.info('{}: {}'.format(k, vars(args)[k]))
    # import sys
    # sys.exit(0)
    from_server = "{}:{}".format(args.from_host, args.from_port)
    from_topic = args.from_topic

    to_server = "{}:{}".format(args.to_host, args.to_port)
    to_topic = args.to_topic

    kafka_to_kafka(from_server, from_topic, to_server, to_topic)


