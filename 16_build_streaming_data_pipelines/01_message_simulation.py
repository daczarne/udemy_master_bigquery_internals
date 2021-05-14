from google.cloud import pubsub_v1
import time

#* Instantiate a publisher client object
publisher = pubsub_v1.PublisherClient()

#* Name of the Topic
topic_name = 'projects/bigquery-demo-285417/topics/data_stream_from_file'

#* Create the topic
try:
	publisher.create_topic(topic_name)
except:
	print('Topic already exists')

#* Simulate message publishing
with open('food_daily.csv') as f_in:
	for line in f_in:
		#* Data must be a bytestring
		data = line
		#* Publish the messages
		future = publisher.publish(topic_name, data = data)
		print(future.result())
		time.sleep(1)
