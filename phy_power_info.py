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
from phystats.collector.power_info import power_info
from phystats.repeat_timer import RepeatTimer
from phystats.kafkah.kafka_helper import KafkaHelper



parser = argparse.ArgumentParser()

parser.add_argument('--kafka_host', default="localhost", type=str, help="kafka host")
parser.add_argument('--kafka_port', default="9092", type=str, help="kafka port")
parser.add_argument('--kafka_topic', default="phystats", type=str, help="kafka topic")
parser.add_argument('--collect_interval', default=5.0, type=float, help="metric collect interval")
parser.add_argument('--cmd_args', default="ipmitool", type=str, nargs='+',help="sudo ipmitool sdr elist")
parser.add_argument('--filters', default="Power", type=str, nargs='+',help="key word to filter raw data")
parser.add_argument('--daemon', action='store_true', help="daemon mod")
parser.add_argument('--daemon_action', default='start', type=str, choices=['start', 'stop'],
                    help="start/stop daemon process")
args = parser.parse_args()


def get_phy_power_info():
    msgs = []
    try:
        msgs = power_info(args.cmd_args, args.filters)
    except Exception as e:
        logger.warn("Get pysical power info failed! Exception: {}".format(e))
    logger.info("Number of physical power information messages: {}".format(len(msgs)))
    for msg in msgs:
        logger.debug("phy_power_info: {}".format(msg))

    kafka_helper = KafkaHelper(topic=args.kafka_topic, host=args.kafka_host, port=args.kafka_port)
    kafka_helper.send_msg_list(msgs, topic=None)


if __name__ == '__main__':
    logger.info("Main thread start!")
    # get_k8s_cluster_info()
    # get_metrics()
    for k in list(vars(args).keys()):
        logger.info('{}: {}'.format(k, vars(args)[k]))
    # import sys
    # sys.exit(0)
    PIDFILE = '/tmp/phy_power_info_daemon.pid'

    if args.daemon:
        if args.daemon_action == 'start':
            try:
                daemonizef(PIDFILE,
                        stdout='/tmp/phy_power_info_daemon.log',
                        stderr='/tmp/phy_power_info_daemon.log')
            except RuntimeError as e:
                print(e, file=sys.stderr)
                raise SystemExit(1)
            # 守护进程中运行的主程序
            power_info_timer = RepeatTimer(args.collect_interval, get_phy_power_info)
            power_info_timer.start()
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
        power_info_timer = RepeatTimer(args.collect_interval, get_phy_power_info)
        power_info_timer.start()