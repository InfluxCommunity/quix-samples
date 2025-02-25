import quixstreams as qx
from percentage_function import PercentageAlert
import os


# Alternatively, you can always pass an SDK token manually as an argument.
client = qx.QuixStreamingClient()

# Change consumer group to a different constant if you want to run model locally.
print("Opening input and output topics")

# Define environmental variables

consumer_topic = client.get_topic_consumer(os.environ["input"], "default-consumer-group")
producer_topic = client.get_topic_producer(os.environ["output"])


def consume_stream(consumer_stream: qx.StreamConsumer):
    # Create a new stream to output data

    producer_stream = producer_topic.get_or_create_stream(consumer_stream.stream_id + '-' + os.environ["Quix__Deployment__Name"])
    producer_stream.properties.parents.append(consumer_stream.stream_id)

    # handle the data in a function to simplify the example
    perc_alert = PercentageAlert(consumer_stream, producer_stream)

    # React to new data received from input topic.
    consumer_stream.timeseries.on_dataframe_received = perc_alert.on_data_frame_handler


    def on_stream_close():
        producer_stream.close()
        print("Stream closed:" + producer_stream.stream_id)

    consumer_stream.on_stream_closed = on_stream_close


# Hook up events before initiating read to avoid losing out on any data

consumer_topic.on_stream_received = consume_stream

# Hook up to termination signal (for docker image) and CTRL-C
print("Listening to streams. Press CTRL-C to exit.")

# Handle graceful exit of the model.
qx.App.run()
