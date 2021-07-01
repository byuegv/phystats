# -*- coding:utf-8 -*-

import os
import sys
import signal
import argparse
import json
import time
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import kafka_errors
from phystats.logger import logger
from phystats.daemonize import daemonizef



parser = argparse.ArgumentParser()

parser.add_argument('--from_host', default="localhost", type=str, help="host of source kafka")
parser.add_argument('--from_port', default="9092", type=str, help="port of source kafka")
parser.add_argument('--from_topic', default="phystats", type=str, help="topic of source kafka")
parser.add_argument('--to_host', default="localhost", type=str, help="host of to kafka")
parser.add_argument('--to_port', default="9092", type=str, help="port of to kafka")
parser.add_argument('--to_topic', default="phystats", type=str, help="topic of to kafka")
parser.add_argument('--daemon', action='store_true', help="daemon mod")
parser.add_argument('--daemon_action', default='start', type=str, choices=['start', 'stop'],
                    help="start/stop daemon process")

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

    PIDFILE = '/tmp/phystats_k2k_daemon.pid'
    if args.daemon:
        if args.daemon_action == 'start':
            try:
                daemonizef(PIDFILE,
                        stdout='/tmp/phystats_k2k_daemon.log',
                        stderr='/tmp/phystats_k2k_daemon.log')
            except RuntimeError as e:
                print(e, file=sys.stderr)
                raise SystemExit(1)
            # 守护进程中运行的主程序
            kafka_to_kafka(from_server, from_topic, to_server, to_topic)

        elif args.daemon_action == 'stop':
            if os.path.exists(PIDFILE):
                with open(PIDFILE) as f:
                    os.kill(int(f.read()), signal.SIGTERM)
            else:
                print('Not running', file=sys.stderr)
                raise SystemExit(1)
        else:
            print('Unknown command {!r}'.format(sys.argv[1]), file=sys.stderr)
            raise SystemExit(1)
    else:
        kafka_to_kafka(from_server, from_topic, to_server, to_topic)


