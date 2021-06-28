# -*- coding:utf-8 -*-

import unittest
from phystats.repeat_timer import RepeatTimer
from phystats.collector.collect import collect_metrics
from phystats.collector.k8s_collector import k8s_cluster_info


class TestCollector(unittest.TestCase):
    def test_collector_metrics(self):
        msgs = collect_metrics(host='localhost', port=9090)
        print(len(msgs))
        for msg in msgs:
            print(msg)
    
    def test_k8s_cluster_info(self):
        msgs = k8s_cluster_info()
        print(len(msgs))
        for msg in msgs:
            print(msg)


if __name__ == '__main__':
    test = TestCollector()
    test.test_collector_metrics()
    test.test_k8s_cluster_info()