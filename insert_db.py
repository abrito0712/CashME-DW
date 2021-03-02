import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

try:
    print("Azure Blob storage v" + __version__ + " - Python quickstart sample")
    # Quick start code goes here
except Exception as ex:
    print('Exception:')
    print(ex)

import pyodbc 
import pandas as pd
from datetime import datetime


#conexão com o DB
server = 'serversqlcashme.database.windows.net' 
database = 'cashme' 
username = 'userconnect' 
password = 'Armagedon07@' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

cursor = cnxn.cursor()

propostas_df = pd.read_csv('/usr/local/airflow/dags/csh_sladeatendimento_transient/SLA.csv', encoding='utf_32', decimal=",")
#deleta a tabela 
sql = ('DELETE FROM SLA')
cursor.execute(sql)
cnxn.commit()

#tratamento dos dados para geração do script do insert
for i,row in propostas_df.iterrows():
   sql = ''
   values = ''
   sqlinsert = ''
   v_id_proposta = str(row['id_proposta'])
   v_tempo_aprovacao = row['tempo_aprovacao']
   v_createdon_quote = str(row['createdon_quote'])
   v_createdon_quote = v_createdon_quote.split('+')
   v_createdon_quote = str(v_createdon_quote[0])
   # v_createdon_quote = datetime.strptime(v_createdon_quote,'%Y-%m-%d %H:%M:%S')
   print(v_createdon_quote)
    
   if v_id_proposta == 'NA' or v_id_proposta == 'nan':
       v_id_proposta = '" ",'
   else:
       v_id_proposta = "'" +  v_id_proposta + "',"

   if v_tempo_aprovacao == 'NA' or v_tempo_aprovacao == 'nan':
       v_tempo_aprovacao = str(0) 
       v_tempo_aprovacao = str(v_tempo_aprovacao) + ','
   else:
       v_tempo_aprovacao = str(v_tempo_aprovacao) + ','

   if v_createdon_quote == 'NA' or v_createdon_quote == 'nan':
       v_createdon_quote = '" ");'        
   else:
       v_createdon_quote = "'" +  v_createdon_quote + "');"
       #v_createdon_quote = str(v_createdon_quote) + ');'
    
           
    
   #Insert no DB     
   sql = 'INSERT INTO SLA (ID_PROPOSTA, TEMPO_APROVACAO, CREATEDON_QUOTE) VALUES ('
   value = v_id_proposta + v_tempo_aprovacao + v_createdon_quote

   sqlinsert = sql + value
   print(sqlinsert)
   cursor.execute(sqlinsert)
   cnxn.commit()

	
	
	
