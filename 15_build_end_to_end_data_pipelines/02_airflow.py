from airflow import models
from datetime import datetime, timedelta
from airflow.contrib.operators.dataflow_operator import DataFlowPythonOperator

#* Default arguments applicable to all operators used in this DAG (unless overwritten)
default_args = {
	'owner': 'Airflow',
	'start_date': datetime(2021, 5, 15),
	'retries': 0,
	'retry_delay': timedelta(seconds = 50),
	'dataflow_default_options': {
		'project': '<project_name>',
		'region': 'us-central1',
		'runner': 'DataflowRunner'
	}
}

#* Instantiate the DAG object. All DAG parameters can be found here https://github.com/apache/airflow/blob/master/airflow/models/dag.py
with models.DAG(
	dag_id = 'food_orders_dag',
	default_args = default_args,
	schedule_interval = '@daily',
	#* Should jobs be backfilled? False means No
	catchup = False
) as dag:
	#* Which tasks should be run? The complete documentation to the Python Operator can be found here http://airflow.apache.org/docs/apache-airflow/1.10.6/_api/airflow/contrib/operators/dataflow_operator/index.html
	t1 = DataFlowPythonOperator(
		task_id = 'beamtask',
		py_file = '<path_to_python_file.py>',
		options = {
			'input': '<input_file_location>'
		}
	)

#! If we need to run more than one task, we can added to the with clause. To set dependencies we use t1 >> t2 to mean that task t2 should be run after task t1 has been completed.
