# -*- coding:utf-8 -*-

import unittest
from phystats.kafka2kafka import kafka_to_kafka


class TestKafka2Kafka(unittest.TestCase):
    def test_k2k(self):
        from_server = "localhost:9092"
        from_topic = "phystats"
        to_server = "localhost:9092"
        to_topic = "phystats"
        kafka_to_kafka(from_server, from_topic, to_server, to_topic)


if __name__ == '__main__':
    test = TestKafka2Kafka()
    test.test_k2k()