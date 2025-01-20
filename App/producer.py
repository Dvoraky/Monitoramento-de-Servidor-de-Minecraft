import requests
from quixstreams import Application

app = Application(
    broker_address="localhost:9092", 
    loglevel="DEBUG", auto_offset_reset="latest", 
    consumer_group="application-name")


with app.get_producer() as producer:
    producer.produce(topic="test", key="coolMsg", value="anotherMsg")