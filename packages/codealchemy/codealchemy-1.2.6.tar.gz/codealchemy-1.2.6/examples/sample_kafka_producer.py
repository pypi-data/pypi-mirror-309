from codealchemy import kafkaUtils

# Initialize producer with the configuration file and topic name
config_file = "config.json"
topic = "topic-1"

producer = kafkaUtils.KafkaProducer(config_file, topic)

# Send messages to default partitions
print("\nProducing Messages to default partition:")
for i in range(10):
    # Construct the message payload
    message = {"key": i, "value": f"Test message {i}"}
    producer.send_message(message)
# Flush to ensure all messages are sent
producer.flush()
print("\nLatest offsets:")
producer.display_partition_offsets()


# Send messages to specific partitions
print("\nProducing Messages to Particular partition:")
for i in range(10):
    # Construct the message payload
    message = {"key": i, "value": f"Test message {i}"}
    producer.send_message(message, partition=1)
producer.flush()
print("\nLatest offsets:")
producer.display_partition_offsets()


# Send messages in a round-robin fashion across partitions
print("\nProducing Messages in Round Robin:")
for i in range(10):
    message = {"key": i, "value": f"Test message {i}"}
    producer.send_message_round_robin(message)
producer.flush()
print("\nLatest offsets:")
producer.display_partition_offsets()
