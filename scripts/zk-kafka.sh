#!/bin/bash

bin/zookeeper-server-start.sh -daemon config/zookeeper.properties
bin/kafka-server-start.sh  -daemon config/server.properties
bin/kafka-topics.sh --create --topic phystats --partitions 1 --replication-factor 1 --bootstrap-server localhost:9092
# bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic phystats --from-beginning

# bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic phystats
# bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic phystats --from-beginning
# bin/kafka-console-producer.sh --broker-list localhost:9092 --topic phystats
# bin/kafka-config.sh --zookeeper localhost:2181 --alter --entity-name phystats --entity_type topics --add-config retention.ms=21600000
# bin/kafka-config.sh --zookeeper localhsot:2181 --describle --entity-name phystats --entity_type topics
# bin/kafka-topic.sh --zookeeper localhost:2181 --alter --topic  phystats --config  cleanup.policy=delete
