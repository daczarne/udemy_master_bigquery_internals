delivered_table_spec = '<project_name>:<dataset_name>.delivered_orders'
other_table_spec = '<project_name>:<dataset_name>.other_status_orders'

#! Import libraries and modules
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
import argparse
from google.cloud import bigquery
from threading import Timer
from apache_beam.runners.runner import PipelineState


#! Utility functions

#* Removes the last colon on the product column
def remove_last_colon(row):
	cols = row.split(',')
	item = str(cols[4])
	if item.endswith(':'):
		cols[4] = item[:-1]
	return ','.join(cols)


#* Removes special characters
def remove_special_characters(row):
	import re
	cols = row.split(',')
	ret = ''
	for col in cols:
		clean_col = re.sub(r'[?%&]', '', col)
		ret = ret + clean_col + ','
		ret = ret[:-1]
	return ret


#* Prints rows
def print_row(row):
	print(row)


#* Build JSON data
def to_json(csv_str):
	fields = csv_str.split(',')
	json_str = {
		"customer_id": fields[0],
		"date": fields[1],
		"timestamp": fields[2],
		"order_id": fields[3],
		"items": fields[4],
		"amount": fields[5],
		"mode": fields[6],
		"restaurant": fields[7],
		"status": fields[8],
		"ratings": fields[9],
		"feedback": fields[10],
		"new_col": fields[11]
	}
	return json_str


#* Creates the view
def create_view():
	print('Creating VIEW thread ...')
	view_name = "daily_food_orders"
	dataset_ref = client.dataset('dataset_food_orders')
	view_ref = dataset_ref.table(view_name)
	view_to_create = bigquery.Table(view_ref)
	view_to_create.view_query = """
		SELECT *
		FROM `<project_name>.<dataset_name>.<source_table_name>`
		WHERE _PARTITIONDATE = DATE(CURRENT_DATE())
	"""
	view_to_create.view_use_legacy_sql = False
	try:
		client.create_table(view_to_create)
	except:
		print('View already exists')


#! Beam pipeline

#* Instantiate an argument parser
parser = argparse.ArgumentParser()

#* Read and parse arguments from command line
parser.add_argument(
	'--input',
	dest = 'input',
	required = True,
	help = 'Input file to process.'
)

path_args, pipeline_args = parser.parse_known_args()
inputs_pattern = path_args.input

#* Set pipeline options
options = PipelineOptions(pipeline_args)
options.view_as(StandardOptions).streaming = True

#* Instantiate the p-collection
p = beam.Pipeline(options = options)

#* Generate the cleaned data p-collection
cleaned_data = (
	p
	| beam.io.ReadFromPubSub(topic = inputs_pattern)
	| beam.Map(remove_last_colon)
	| beam.Map(lambda row: row.lower())
	| beam.Map(remove_special_characters)
	| beam.Map(lambda row: row + ',1')
)

delivered_orders = (
	cleaned_data
	| 'delivered filter' >> beam.Filter(lambda row: row.split(',')[8].lower() == 'delivered')
)

other_orders = (
	cleaned_data
	| 'Undelivered Filter' >> beam.Filter(lambda row: row.split(',')[8].lower() != 'delivered')
)


#! BigQuery pipeline

client = bigquery.Client()
dataset_id = "{}.dataset_food_orders".format(client.project)

try:
	client.get_dataset(dataset_id)
except:
	dataset = bigquery.Dataset(dataset_id)
	dataset.location = "US"
	dataset.description = "dataset for food orders"
	dataset_ref = client.create_dataset(dataset, timeout = 30)


table_schema = 'customer_id:STRING,date:STRING,timestamp:STRING,order_id:STRING,items:STRING,amount:STRING,mode:STRING,restaurant:STRING,status:STRING,ratings:STRING,feedback:STRING,new_col:STRING'

(
	delivered_orders
	| 'delivered to json' >> beam.Map(to_json)
	| 'write delivered' >> beam.io.WriteToBigQuery(
		delivered_table_spec,
		schema = table_schema,
		create_disposition = beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
		write_disposition = beam.io.BigQueryDisposition.WRITE_APPEND,
		additional_bq_parameters = {
			'timePartitioning': {'type': 'DAY'}
		}
	)
)

(
	other_orders
	| 'others to json' >> beam.Map(to_json)
	| 'write other_orders' >> beam.io.WriteToBigQuery(
		other_table_spec,
		schema = table_schema,
		create_disposition = beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
		write_disposition = beam.io.BigQueryDisposition.WRITE_APPEND,
		additional_bq_parameters = {
			'timePartitioning': {'type': 'DAY'}
		}
	)
)

#* Create the view in a new thread. Every 25 seconds the View will be refreshed.
t = Timer(25.0, create_view)
t.start()

#* Run the pipeline until it finishes (its not supposed to finnish 😂)
ret = p.run()
ret.wait_until_finish()

if ret.state == PipelineState.DONE:
	print('Success!!!')
else:
	print('Error Running beam pipeline')
