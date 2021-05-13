#* Names of the tables to which data is going to be uploaded
delivered_table_spec = '<project_name>:<dataset_name>.delivered_orders'
other_table_spec = '<project_name>:<dataset_name>.other_status_orders'

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
import argparse
from google.cloud import bigquery

#* Create an argument parser object
parser = argparse.ArgumentParser()

#* Define how the arguments are going to be passed in the command line. In this case just an input argument will be supplied with the path to the CSV file that contains that data.
parser.add_argument(
	'--input',
	dest = 'input',
	required = True,
	help = 'Path to input file to process.'
)

path_args, pipeline_args = parser.parse_known_args()

#* Set the pattern to get the input command (in this case 'input')
inputs_pattern = path_args.input

#* Get the pipeline options. These are the environment configurations
options = PipelineOptions(pipeline_args)

#* Instance of pipeline class
p = beam.Pipeline(options = options)


#* Use case specific transformations. These functions will clean the data.

#* This function removes the colon at the end of the row
def remove_last_colon(row):
	cols = row.split(',')
	item = str(cols[4])
	if item.endswith(':'):
		cols[4] = item[:-1]
	return ','.join(cols)


#* This function removes all special characters. It replaces them for an empty string
def remove_special_characters(row):
	import re
	cols = row.split(',')
	ret = ''
	for col in cols:
		clean_col = re.sub(r'[?%&]', '', col)
		ret = ret + clean_col + ','
		ret = ret[:-1]
	return ret


def print_row(row):
	print(row)


#* Create a collection that uses the pipeline options and runs the cleaning transformations on it. We start with the p object and then use the | (pipeline operator) to apply transformations to the data
cleaned_data = (
	p
	#* Read the data
	| beam.io.ReadFromText(inputs_pattern, skip_header_lines = 1)
	#* Remove the last colon
	| beam.Map(remove_last_colon)
	#* Make everything lower case
	| beam.Map(lambda row: row.lower())
	#* Remove special characters
	| beam.Map(remove_special_characters)
	#* It adds a column of 1s at the end of the row
	| beam.Map(lambda row: row + ',1')
)


#* Delivered orders collection
delivered_orders = (
	cleaned_data
	| 'delivered filter' >> beam.Filter(lambda row: row.split(',')[8].lower() == 'delivered')
)

#* Other orders collection (status not delivered)
other_orders = (
	cleaned_data
  | 'Undelivered Filter' >> beam.Filter(lambda row: row.split(',')[8].lower() != 'delivered')
)

#* This is just of testing purposed. Take the counts and compare them.
(
	cleaned_data
	#* Count all elements in the cleaned_data p-collection
	| 'count total' >> beam.combiners.Count.Globally()
	| 'total map' >> beam.Map(lambda x: 'Total Count:' + str(x))
	| 'print total' >> beam.Map(print_row)
)

(
	delivered_orders
	| 'count delivered' >> beam.combiners.Count.Globally()
	| 'delivered map' >> beam.Map(lambda x: 'Delivered count:' + str(x))
	| 'print delivered count' >> beam.Map(print_row)
)

(
	other_orders
	| 'count others' >> beam.combiners.Count.Globally()
	| 'other map' >> beam.Map(lambda x: 'Others count:' + str(x))
	| 'print undelivered' >> beam.Map(print_row)
)


#! ################################################################################################ !#
#! At this point, the data has been read and cleaned! Data is now ready to be loaded onto BigQuery. !#
#! ################################################################################################ !#


#* Create a BigQuery client instance. 
client = bigquery.Client()

dataset_id = "{}.dataset_food_orders".format(client.project)

try:
	client.get_dataset(dataset_id)
except:
	dataset = bigquery.Dataset(dataset_id)  #
	dataset.location = "US"
	dataset.description = "dataset for food orders"
	dataset_ref = client.create_dataset(dataset, timeout=30)  # Make an API request.

def to_json(csv_str):
	fields = csv_str.split(',')
	json_str = {
		"customer_id":fields[0],
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

table_schema = 'customer_id:STRING,date:STRING,timestamp:STRING,order_id:STRING,items:STRING,amount:STRING,mode:STRING,restaurant:STRING,status:STRING,ratings:STRING,feedback:STRING,new_col:STRING'

(
	delivered_orders
	| 'delivered to json' >> beam.Map(to_json)
	| 'write delivered' >> beam.io.WriteToBigQuery(
		delivered_table_spec,
		schema = table_schema,
		create_disposition = beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
		write_disposition = beam.io.BigQueryDisposition.WRITE_APPEND,
		additional_bq_parameters = {'timePartitioning': {'type': 'DAY'}}
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
		additional_bq_parameters = {'timePartitioning': {'type': 'DAY'}}
	)
)

from apache_beam.runners.runner import PipelineState

ret = p.run()

if ret.state == PipelineState.DONE:
	print('Success!!!')
else:
	print('Error Running beam pipeline')


view_name = "daily_food_orders"
dataset_ref = client.dataset('dataset_food_orders')
view_ref = dataset_ref.table(view_name)
view_to_create = bigquery.Table(view_ref)

view_to_create.view_query = 'select * from `bigquery-demo-285417.dataset_food_orders.delivered_orders` where _PARTITIONDATE = DATE(current_date())'
view_to_create.view_use_legacy_sql = False

try:
	client.create_table(view_to_create)
except:
	print('View already exists')
