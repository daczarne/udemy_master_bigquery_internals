#! Import libraries and modules

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
import argparse
from google.cloud import bigquery
from apache_beam.runners.runner import PipelineState


#! Table specs
#* Names of the tables to which data is going to be uploaded
delivered_table_spec = '<project_name>:<dataset_name>.delivered_orders'
other_table_spec = '<project_name>:<dataset_name>.other_status_orders'


#! Use case specific transformations. These functions will clean the data.

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

#* Print rows
def print_row(row):
	print(row)


#* Transform data to JSON format
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


#! #################### !#
#! Apache Beam pipeline !#
#! #################### !#


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
  | 'undelivered filter' >> beam.Filter(lambda row: row.split(',')[8].lower() != 'delivered')
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

#* Create the dataset
dataset_id = "{}.<dataset_name>".format(client.project)

try:
	client.get_dataset(dataset_id)
except:
	dataset = bigquery.Dataset(dataset_id)
	dataset.location = "US"
	dataset.description = "dataset for food orders"
	dataset_ref = client.create_dataset(dataset, timeout=30)


#* Define table schema (needs to be the same as the JSON)
table_schema = 'customer_id:STRING,date:STRING,timestamp:STRING,order_id:STRING,items:STRING,amount:STRING,mode:STRING,restaurant:STRING,status:STRING,ratings:STRING,feedback:STRING,new_col:STRING'

#* Use the WriteToBigQuery method to load the data con delivered orders. You can find the complete documentation for this methon here https://beam.apache.org/releases/pydoc/2.15.0/apache_beam.io.gcp.bigquery.html
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

#* Use the WriteToBigQuery method to load the data con other orders
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

#* Run
ret = p.run()

#* Print the status of the operation
if ret.state == PipelineState.DONE:
	print('Success!!!')
else:
	print('Error Running beam pipeline')


#! ################################# !#
#! Create a view of delivered orders !#
#! ################################# !#

#* View definitions
view_name = "<view_name>"
dataset_ref = client.dataset('<dataset_name_where_the_view_will_be_created>')
view_ref = dataset_ref.table(view_name)
view_to_create = bigquery.Table(view_ref)

#* View creation query
view_to_create.view_query = """
	SELECT *
	FROM `<project_name>.<dataset_name>.<source_table_name>`
	WHERE _PARTITIONDATE = DATE(CURRENT_DATE())
"""

view_to_create.view_use_legacy_sql = False

#* Use Try-Catch so that it does not fail on subsequent runs
try:
	client.create_table(view_to_create)
except:
	print('View already exists')
