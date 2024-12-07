from codealchemy import kafkaUtils

# Initialize consumer with the configuration file, topic name, and group ID
config_file = "config.json"
topic = "topic-1"
group_id = "group_id"

auto_offset = "earliest"
# earliest -->Start from the beginning if no previous offset exists
# latest -->Start from the end if no previous offset exists

consumer = kafkaUtils.KafkaConsumer(config_file, topic, group_id)

# Press enter to start the consuming message
input("Press Enter to start consuming messages...")

# Start consuming messages and various options

consumer.consume_messages()
# consumer.consume_messages(partition=1, offset=2413)
# consumer.consume_messages(offset=2143)
# consumer.consume_messages(timestamp="2024-11-13T22:39:00.999Z", partition=1)
# consumer.consume_messages(timestamp="2024-11-13T22:39:00.999Z")
