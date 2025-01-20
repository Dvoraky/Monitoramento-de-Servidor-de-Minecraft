from quixstreams import Application

app = Application(broker_address="localhost:9092", loglevel="DEBUG")

with app.get_consumer() as consumer: #write-only connection
    consumer.subscribe(["test"])
    while True:
        msg = consumer.poll(1)
        if msg:
            if msg.error() is None:
                print(msg.value())