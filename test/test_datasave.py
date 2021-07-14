# -*- coding:utf-8 -*-

import unittest
from phystats.datasave import data_save


class TestDataSave(unittest.TestCase):
    def test_datasave(self):
        from_server = "localhost:9092"
        from_topic = "phystats"
        file_prefix = "/data/vm-con"
        limit = 100
        data_save(from_server, from_topic, file_prefix, limit)


if __name__ == '__main__':
    test = TestDataSave()
    test.test_datasave()