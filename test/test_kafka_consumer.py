# -*- coding:utf-8 -*-

import unittest
from phystats.repeat_timer import RepeatTimer
from phystats.kafkah.kafka_helper import KafkaHelper


class TestKafkaConsume(unittest.TestCase):
    def test_consume_msgs(self):
        topic = "phystats"
        host = 'localhost'
        port = 9092
        kafka_helper = KafkaHelper(topic=topic, host=host, port=port)
        msgs = kafka_helper.consume_data(topic=None, boot_server=None, limit=None)
        print(len(msgs))


if __name__ == '__main__':
    test = TestKafkaConsume()
    test.test_consume_msgs()