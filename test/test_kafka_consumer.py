# -*- coding:utf-8 -*-

import unittest
from phystats.repeat_timer import RepeatTimer
from phystats.hkafka.kafka_helper import KafkaHelper


class TestKafkaConsume(unittest.TestCase):
    def test_consume_msgs(self):
        kafka_helper = KafkaHelper(topic="phystats", host='localhost', port=9092)
        msgs = kafka_helper.consume_data(topic=None, boot_server=None, limit=None)
        print(len(msgs))


if __name__ == '__main__':
    test = TestKafkaConsume()
    test.test_consume_msgs()