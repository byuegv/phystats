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
parser.add_argument('--file_prefix', default="vm-con-data", type=str, help="prefix of file name")
parser.add_argument('--limit', default=1000000, type=int, help="msgs of each file")
parser.add_argument('--daemon', action='store_true', help="daemon mod")
parser.add_argument('--daemon_action', default='start', type=str, choices=['start', 'stop'],
                    help="start/stop daemon process")

args = parser.parse_args()


def data_save(from_server, from_topic, file_prefix, limit):
    consumer = KafkaConsumer(from_topic, bootstrap_servers=from_server)    
    logger.info("Start consume data from server={}, topic={}".format(from_server, from_topic))
    cur_count = 1
    while True:
        file_name = "{}-{}.txt".format(file_prefix, cur_count-1)
        with open(file_name, 'a') as f:
            for msg in consumer:
                cur_count += 1
                try:
                    _msg_value = str(msg.value, encoding="utf8").replace('"', '')
                    f.write("{}\n".format(_msg_value))
                    logger.debug("{} {} {}".format(msg.topic, msg.offset, _msg_value))
                except Exception as e:
                    logger.error("Save msg={} to file {} failed!".format(_msg_value, to_server))
                if cur_count % limit == 0:
                    break


if __name__ == '__main__':
    logger.info("Main thread start!")
    for k in list(vars(args).keys()):
        logger.info('{}: {}'.format(k, vars(args)[k]))
    # import sys
    # sys.exit(0)
    from_server = "{}:{}".format(args.from_host, args.from_port)
    from_topic = args.from_topic

    file_prefix = args.file_prefix
    limit = args.limit

    PIDFILE = '/tmp/data_save_daemon.pid'
    if args.daemon:
        if args.daemon_action == 'start':
            try:
                daemonizef(PIDFILE,
                        stdout='/tmp/data_save_daemon.log',
                        stderr='/tmp/data_save_daemon.log')
            except RuntimeError as e:
                print(e, file=sys.stderr)
                raise SystemExit(1)
            # 守护进程中运行的主程序
            data_save(from_server, from_topic, file_prefix, limit)

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
        data_save(from_server, from_topic, file_prefix, limit)


