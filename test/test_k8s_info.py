# -*- coding:utf-8 -*-

import unittest
from phystats.collector.k8s_collector import k8s_cluster_info


class TestK8sInfo(unittest.TestCase):
    
    def test_k8s_cluster_info(self):
        msgs = k8s_cluster_info()
        print(len(msgs))
        for msg in msgs:
            print(msg)


if __name__ == '__main__':
    test = TestK8sInfo()
    test.test_k8s_cluster_info()