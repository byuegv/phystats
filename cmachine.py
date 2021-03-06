# -*- coding:utf-8 -*-

import os
import sys
import signal
import argparse
from phystats.logger import logger
from phystats.collector.machine import collect_metrics
from phystats.collector.k8s_collector import k8s_cluster_info
from phystats.repeat_timer import RepeatTimer
from phystats.kafkah.kafka_helper import KafkaHelper
from phystats.daemonize import daemonizef


parser = argparse.ArgumentParser()

parser.add_argument('--host', default="localhost", type=str, help="prometheus host")
parser.add_argument('--port', default="9090", type=str, help="prometheus port")
parser.add_argument('--kafka_host', default="localhost", type=str, help="kafka host")
parser.add_argument('--kafka_port', default="9092", type=str, help="kafka port")
parser.add_argument('--kafka_topic', default="phystats", type=str, help="kafka topic")
parser.add_argument('--collect_interval', default=5.0, type=float, help="metric collect interval")
parser.add_argument('--consume_interval', default=5.0, type=float, help="kafka interval")
parser.add_argument('--k8s_interval', default=15.0, type=float, help="k8s cluster info collect interval")
parser.add_argument('--limit', default=100000, type=int, help="msgs to consume at once")
parser.add_argument('--role', default="collector", type=str,
                    help="The role of current: collector to get prometheus metrics" +
                         " k8s_info to get k8s_cluster_info" +
                         " consumer to consume msgs from kafka")
parser.add_argument('--daemon', action='store_true', help="daemon mod")
parser.add_argument('--daemon_action', default='start', type=str, choices=['start', 'stop'],
                    help="start/stop daemon process")


args = parser.parse_args()


def get_metrics():
    try:
        msgs = collect_metrics(host=args.host, port=args.port)
        logger.info("Number of metrics messages: {}".format(len(msgs)))
        for msg in msgs:
            logger.debug("metrics: {}".format(msg))
            
        kafka_helper = KafkaHelper(topic=args.kafka_topic, host=args.kafka_host, port=args.kafka_port)
        kafka_helper.send_msg_list(msgs, topic=None)
    except Exception as e:
        logger.warn("Catch Exception when get metrics, Exception: {}".format(e))


if __name__ == '__main__':
    logger.info("Main thread start!")
    # get_k8s_cluster_info()
    # get_metrics()
    for k in list(vars(args).keys()):
        logger.info('{}: {}'.format(k, vars(args)[k]))
    # import sys
    # sys.exit(0)
    PIDFILE = '/tmp/phystats_machine_daemon.pid'

    role = args.role.strip().split(",")

    if args.daemon:
        if args.daemon_action == 'start':
            try:
                daemonizef(PIDFILE,
                        stdout='/tmp/phystats_machine_daemon.log',
                        stderr='/tmp/phystats_machine_daemon.log')
            except RuntimeError as e:
                print(e, file=sys.stderr)
                raise SystemExit(1)
            # ?????????????????????????????????
            collect_timer = RepeatTimer(args.collect_interval, get_metrics)
            collect_timer.start()
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
        collect_timer = RepeatTimer(args.collect_interval, get_metrics)
        collect_timer.start()

