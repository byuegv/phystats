# -*- coding:utf-8 -*-

import unittest
from phystats.collector.power_info import power_info


class TestPhyPowerInfo(unittest.TestCase):
    
    def test_power_info(self):
        cmd_args = ['sudo', 'ipmitool', 'sdr', 'elist']
        filters = ['P', 'Watte']
        msgs = power_info(cmd_args, filters)
        print(len(msgs))
        for msg in msgs:
            print(msg)


if __name__ == '__main__':
    test = TestPhyPowerInfo()
    test.test_power_info()