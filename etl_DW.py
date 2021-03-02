from airflow import DAG 
from datetime import datetime, timedelta 
import airflow 
from airflow.utils.dates import days_ago 
from airflow.operators.bash_operator import BashOperator 
from airflow.operators.dummy_operator import DummyOperator 




# Argumentos básicos de uma DAG 
default_args = { 
				 'start_date':datetime(2021, 2, 22), 
                 'owner':'CashmeDW',  
				 'depends_on_past': False,  
				 'email': ['alexandre.brito@luminiitsolutions.com'],  
				 'email_on_failure': False,  
				 'email_on_retry': False
				} 


###### DAG #########  
with DAG(dag_id='etl-DW',  
    	default_args=default_args, 

		# schedule_interval irá executar apenas uma vez por dia sempre as 07:00 UTC da manhã.
		schedule_interval='00 07 * * *') as dag:

		start = DummyOperator(task_id='start') 

		ingestao_container = BashOperator(task_id='insgestao_container',
					  bash_command="python3 /usr/local/airflow/dags/ingestao_container.py")

		resultado_transient_csh_analisedecredito = BashOperator(task_id='resultado_transient_csh_analisedecredito',
					  bash_command="python3 /usr/local/airflow/dags/resultado_transient_csh_analisedecredito.py")
		
		insert_db = BashOperator(task_id='insert_db',
					  bash_command="python3 /usr/local/airflow/dags/insert_db.py")
		
						  
		end = DummyOperator(task_id='end') 

		

#start >>  ingestao >> motor >> resultado_motor >> Insert_DataLakeGen2_AzureSQL >> end
#start >>  ingestao_container >> end
start >> ingestao_container >> resultado_transient_csh_analisedecredito >> insert_db >> end
