import os, uuid, sys
sys.path.append(' /usr/local/lib/python3.8/site-packages')
#sys.path.append(' /usr/local/lib/python3.6/dist-packages')
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core._match_conditions import MatchConditions
from azure.storage.filedatalake._models import ContentSettings
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
try:
    print("Azure Blob storage v" + __version__ + " - Python quickstart sample")
    # Quick start code goes here
except Exception as ex:
    print('Exception:')
    print(ex)
#Path do container onde os dados ficarão disponíveis 
storage_account_name = "cashmedatalakestorage"
storage_account_key = "GngQc09I1CqgAtwT6txTntxz5HOpT4VauQhO0nXyEJnaI6XV4aJ/Gd1ay8ZNvH7a/4mH9LIeNcjOOmOB6h3urg=="
storage_file_system = "commondataservice-cashmeproduo-org20b9da07"

#Pastas
entities = ["account", "contact", "csh_analisecredito", "csh_sladeatendimento", "quote", "salesorder"]

#Função onde os arquivos são lidos 
#Hoje está local mas será disponibilizado pelo cloud
def download_file(file_system_client, upstream_path):
    #local_file = open("data/raw/{}".format(upstream_path),'wb')
    local_file = open("/usr/local/airflow/dags/{}".format(upstream_path),'wb')
    file_client = file_system_client.get_file_client(upstream_path)
    print("Dowloading {}...".format(upstream_path))
    downloaded_bytes = file_client.download_file().readall()
    print("Dowloaded {}".format(upstream_path))
    local_file.write(downloaded_bytes)
    local_file.close()

#Leitura dos arquivos model e gravação na pasta 
try:  
    service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format("https", storage_account_name), credential=storage_account_key)
    file_system_client = service_client.get_file_system_client(file_system=storage_file_system)
    download_file(file_system_client, "model.json")
    for entity in entities:
        download_file(file_system_client, "{}/2020.csv".format(entity))

except Exception as e:
    print(e)