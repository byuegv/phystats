# -*- coding:utf-8 -*-

import unittest
from phystats.collector.machine import collect_metrics


class TestMACollector(unittest.TestCase):
    def test_collector_metrics(self):
        msgs = collect_metrics(host='localhost', port=9090)
        print(len(msgs))
        for msg in msgs:
            print(msg)


if __name__ == '__main__':
    test = TestMACollector()
    test.test_collector_metrics()
