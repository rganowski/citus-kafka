import json
from datetime import datetime

from kafka import KafkaConsumer

consumer = KafkaConsumer(
    bootstrap_servers=['localhost:19093', 'localhost:29093'],
    # Requesting all already existing topic entries (defaults to those appearing after subscribing) 
    auto_offset_reset="earliest",
    auto_commit_interval_ms=1000,
    enable_auto_commit=True,
    value_deserializer=lambda value: json.loads(value) if value else None,
    # You may also want to play with groups for checking consumers with the same or different group working concurrently
    # group_id="group_name",
)

# This could be done as a part of KafkaConnect creation. Here we can utilize regex patterns. Worth to know.
consumer.subscribe(pattern="table_1")

operations = {'c': 'INSERT', 'u': 'UPDATE', 'd': 'DELETE', 'r': 'INIT'}

try:
    for msg in consumer:
        if msg.value:
            op = operations[msg.value['payload']['op']]
            print(
                f"P{msg.partition}: {datetime.fromtimestamp(msg.timestamp/1000)}: "
                f"{op}: "
                f"{msg.value['payload']['before'] if op == 'DELETE' else msg.value['payload']['after']}"
            )
except KeyboardInterrupt:
    print("…Bye")
