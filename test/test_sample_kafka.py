# -*- coding:utf-8 -*-

import unittest
from phystats.samplekafka import sample_kafka


class TestSampleKafka(unittest.TestCase):
    def test_samplekafka(self):
        from_server = "localhost:9092"
        from_topic = "phystats"
        to_server = "localhost:9092"
        to_topic = "phystats"
        sample_ratio = 0.2
        sample_kafka(from_server, from_topic, to_server, to_topic, sample_ratio=sample_ratio)


if __name__ == '__main__':
    test = TestSampleKafka()
    test.test_samplekafka()