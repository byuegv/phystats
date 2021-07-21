# -*- coding:utf-8 -*-

import os
import sys
import signal
import argparse
import json
import time
import random
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import kafka_errors
from phystats.logger import logger
from phystats.daemonize import daemonizef



parser = argparse.ArgumentParser()

parser.add_argument('--bootstrap_servers', default='localhost:9092', type=str,
                    help="list of kafka servers: host[:port]")
parser.add_argument('--to_topic', default="phystats", type=str, help="kafka topic")

parser.add_argument('--from_bootstrap_servers', default='localhost:9092', type=str,
                    help="kafka source, list of kafka servers: host[:port]")
parser.add_argument('--from_topic', default="phystats", type=str, help="source topic, kafka topic")

parser.add_argument('--daemon', action='store_true', help="daemon mod")
parser.add_argument('--daemon_action', default='start', type=str, choices=['start', 'stop'],
                    help="start/stop daemon process")
parser.add_argument('--sample_ratio', default=1.5, type=float, help="fraction of sample")




args = parser.parse_args()


def kafka_to_kafka(from_servers, from_topic, to_servers, to_topic, sample_ratio=1.5):
    consumer = KafkaConsumer(from_topic, bootstrap_servers=from_servers)
    
    producer =KafkaProducer(bootstrap_servers=to_servers, retries=3,
                            key_serializer=lambda k: json.dumps(k).encode('utf8'),
                            value_serializer=lambda v: json.dumps(v).encode('utf8'))
        
    logger.info("Start consume data from server={}, topic={}".format(from_server, from_topic))
    while True:
        cur_count = 0
        for msg in consumer:
            cur_count += 1
            _msg_value = str(msg.value, encoding="utf8").replace('"', '')
            logger.debug("{} {} {}".format(msg.topic, msg.offset, _msg_value))
            try:
                rand = random.random()
                if rand < sample_ratio:
                    logger.debug("Start send data to server={}, topic={}".format(to_servers, to_topic))
                    future = producer.send(to_topic, value=_msg_value)
            except Exception as e:
                logger.error("Send msg={} to kafka {} failed! Exception: {}".format(_msg_value, to_servers, e))


if __name__ == '__main__':
    logger.info("Main thread start!")
    for k in list(vars(args).keys()):
        logger.info('{}: {}'.format(k, vars(args)[k]))
    # import sys
    # sys.exit(0)
    from_servers = args.from_bootstrap_servers.strip().split(",")
    from_topic = args.from_topic

    to_servers = args.bootstrap_servers.strip().split(",")
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
            kafka_to_kafka(from_servers, from_topic, to_servers, to_topic, sample_ratio=args.sample_ratio)

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
        kafka_to_kafka(from_servers, from_topic, to_servers, to_topic, sample_ratio=args.sample_ratio)


