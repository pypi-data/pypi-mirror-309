# CodeAlchemy

[![PyPI version](https://img.shields.io/pypi/v/codealchemy)](https://pypi.org/project/codealchemy/)
![License](https://img.shields.io/pypi/l/codealchemy)
![Python versions](https://img.shields.io/pypi/pyversions/codealchemy)

`CodeAlchemy` is a versatile Python package designed to simplify development workflows by providing powerful decorators for logging, performance monitoring, and utilities. Whether you're looking to track function execution times, group logs for better readability, or Utility methods to interact with other services.

### Key Features:

- **Decorators**: Enhance your Python functions with performance tracking and logging capabilities.
- **Kafka Utilities**: Easily produce and consume messages with Kafka, with advanced features like round-robin message distribution and offset management.

## Installation

You can install `codealchemy` using pip:

```sh
pip install codealchemy
```

## Usage

Here is how you can use the `codealchemy` package in your Python code:

### Decorators

- **`code_execution_time`**: This decorator logs the execution time of the decorated function.
- **`log_group(group_name)`**: This decorator logs entry and exit points of the decorated function, grouping logs under a specified group name.

1. code execution time

```python
from codealchemy import code_execution_time

@code_execution_time
def example_function():
    import time
    time.sleep(2)
    print("Function executed")

example_function()
```

2. Log groups

```python

from codealchemy import log_group
import logging

# Ensure the logger level is set to INFO
logging.getLogger(__name__).setLevel(logging.INFO)

@log_group("MainGroup")
def main_function():
    print("Inside main function")
    print("*"*20)
    logging.info("Inside main function")
    inner_function()

@log_group("InnerGroup")
def inner_function():
    print("Inside inner function")
    print("*"*20)
    logging.info("Inside inner function")
    innermost_function()

@log_group("InnermostGroup")
def innermost_function():
    print("Inside innermost function")
    print("*"*20)
    logging.info("Inside innermost function")
    print("Innermost function executed")

main_function()
```

![image](https://github.com/user-attachments/assets/15495373-711d-4b72-9fbb-32acb80c110b)

### Utility

- **`kafkaUtils`**: A utility module that simplifies Kafka-related operations for Python developers.

1. Kafka Producer:
   The Kafka producer sends messages to Kafka topics. Here's how you can use it:

   ```python
   from codealchemy import kafkaUtils

   config_file = "config.json"
   topic = "topic_name"

   producer = kafkaUtils.KafkaProducer(config_file, topic)


   print("\nProducing Messages to default partition:")
   # Send messages to default partitions
   for i in range(10):
       # Construct the message payload
       message = {"key": i, "value": f"Test message {i}"}
       producer.send_message(message)
   # Flush to ensure all messages are sent
   producer.flush()
   print("\nLatest offsets:")
   producer.display_partition_offsets()


   print("\nProducing Messages to Particular partition:")
   # Send messages to specific partitions
   for i in range(10):
       # Construct the message payload
       message = {"key": i, "value": f"Test message {i}"}
       producer.send_message(message, partition=1)
   producer.flush()
   print("\nLatest offsets:")
   producer.display_partition_offsets()


   print("\nProducing Messages in Round Robin:")
   # Send messages in a round-robin fashion across partitions
   for i in range(10):
       message = {"key": i, "value": f"Test message {i}"}
       producer.send_message_round_robin(message)
   producer.flush()
   print("\nLatest offsets:")
   producer.display_partition_offsets()
   ```

2. Kafka Consumer:
   The Kafka consumer consumes messages from Kafka topics. Here's how you can use it:

   ```python
   from codealchemy import kafkaUtils

   config_file = "config.json"
   topic = "topic_name"
   group_id = "group_id"

   auto_offset = "earliest"
    # earliest -->Start from the beginning if no previous offset exists
    # latest -->Start from the end if no previous offset exists

   consumer = kafkaUtils.KafkaConsumer(config_file, topic, group_id, auto_offset)
   consumer.consume_messages()

   ```

   If you need to consume from particular offset

   ```python
   consumer = kafkaUtils.KafkaConsumer(config_file, topic, group_id)
   consumer.consume_messages(offset=2350, partition=1)
   # consumer.consume_messages(offset=2350) # For all partition
   ```

   If you need to consume from particular timestamp

   ```python
   consumer = kafkaUtils.KafkaConsumer(config_file, topic, group_id)
   consumer.consume_messages(timestamp="2024-11-13T22:39:00.999Z", partition=1)
   # consumer.consume_messages(timestamp="2024-11-13T22:39:00.999Z") # For all partition
   ```

   If you need to list all the Consumer Group Offset

   > [!NOTE]
   > Before running the below code try to increase the ulimit for the number of open file descriptors `ulimit -n 1048575` since it will be running using threadpool executor

   ```python
   consumer_info = kafkaUtils.KafkaConsumer(config_file, topic)
   consumer_info.list_consumer_groups_offsets()
   ```

   Sample `config.json`

   ```json
   {
     "bootstrap.servers": "kafkabroker:9093",
     "security.protocol": "SSL",
     "ssl.key.password": "Password@1",
     "ssl.certificate.location": "/etc/secrets/kafka/truststore.pem",
     "ssl.key.location": "/etc/secrets/kafka/keystore.pem",
     "ssl.ca.location": "/etc/secrets/kafka/caroot.pem"
   }
   ```

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.
