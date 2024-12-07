from codealchemy import kafkaUtils

# Initialize consumer with the configuration file, topic name, and group ID
config_file = "config.json"
topic = "topic-1"

consumer = kafkaUtils.KafkaConsumer(config_file, topic)
consumer.list_consumer_groups_offsets()
