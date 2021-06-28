# -*- coding:utf-8 -*-

from phystats.logger import logger
from phystats.collector.collect import collect_metrics
from phystats.repeat_timer import RepeatTimer

def get_metrics():
    msgs = collect_metrics()
    print(len(msgs))

if __name__ == '__main__':
    logger.info("Main thread start!")
    get_metrics()
    # collect_timer = RepeatTimer(5.0, get_metrics)

