"""create topic"""
from typing import List
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException

TOPIC1 = "RawMotMeta"
TOPIC2 = "RawFaceMeta"
TOPIC100 = "RawImage"
TOPIC3 = "Filtered"
TOPIC4 = "Matched"
TOPIC5 = "Mtmc"
TOPIC6 = "Event"
TOPIC101 = "Display"
TOPIC7 = "Forsave"
TOPIC8 = "Saved"

admin_client = AdminClient(
    {
        "bootstrap.servers": "tainp.local:9092",
    }
)

topic_list: List[NewTopic] = [
    NewTopic(topic=TOPIC1, num_partitions=1, replication_factor=1),
    NewTopic(topic=TOPIC2, num_partitions=1, replication_factor=1),
    NewTopic(topic=TOPIC3, num_partitions=1, replication_factor=1),
    NewTopic(topic=TOPIC4, num_partitions=1, replication_factor=1),
    NewTopic(topic=TOPIC5, num_partitions=1, replication_factor=1),
    NewTopic(topic=TOPIC6, num_partitions=1, replication_factor=1),
    NewTopic(topic=TOPIC7, num_partitions=1, replication_factor=1),
    NewTopic(topic=TOPIC8, num_partitions=1, replication_factor=1),
    NewTopic(
        topic=TOPIC100,
        num_partitions=1,
        replication_factor=1,
        config={"retention.ms": 5 * 60 * 1000},  # 5 minutes in miliseconds
    ),
    NewTopic(
        topic=TOPIC101,
        num_partitions=1,
        replication_factor=1,
        config={"retention.ms": 5 * 60 * 1000},  # 5 minutes in miliseconds
    ),
]

# validate before doing anything
admin_client.create_topics(new_topics=topic_list, validate_only=True)

# now create the topic actually
topic_creation_results = admin_client.create_topics(new_topics=topic_list, validate_only=False)

# Wait for each operation to finish.
for topic, f in topic_creation_results.items():
    try:
        f.result()  # The result itself is None
        print(f"Topic {topic} created with status {f.result()}")
    except KafkaException as e:
        print(f"Failed to create topic {topic}: {e}")

# now list all topics
cluster_meta = admin_client.list_topics()
for key, value in cluster_meta.topics.items():
    if not key.startswith("_"):
        print(key, value)
