import pandas as pd 
import numpy as np
import datetime

#Como definido, o modelo foi o SLA
propostas_df = pd.read_csv('/usr/local/airflow/dags/propostas.csv', encoding='utf_32', decimal=",")


def to_date(df):
    return df.dt.date


target_time_field_name = 'csh_datahoraaprovacaocomite'
aprovadas = propostas_df.dropna(subset=[target_time_field_name])

aprovadas = propostas_df.dropna(subset=[target_time_field_name])
#Propostas maior que 2020-06
aprovadas = aprovadas[aprovadas.createdon_quote > '2020-06']
aprovadas[target_time_field_name] = pd.to_datetime(aprovadas[target_time_field_name])
aprovadas['createdon_quote'] = pd.to_datetime(aprovadas['createdon_quote'])

#esses foram os campos escolhidos para serm enviados ao DB e agrupados
aprovadas = aprovadas.groupby(['id_proposta', 'createdon_quote', 'mes_criacao_proposta', target_time_field_name]).count().reset_index()
aprovadas = aprovadas.dropna()
aprovadas['tempo_aprovacao'] = np.busday_count(to_date(aprovadas['createdon_quote']), to_date(aprovadas[target_time_field_name]))


print(aprovadas[aprovadas.mes_criacao_proposta == '2020-11'][['id_proposta', 'tempo_aprovacao', 'createdon_quote']].dropna())

dfresult = aprovadas[aprovadas.mes_criacao_proposta == '2020-11'][['id_proposta', 'tempo_aprovacao', 'createdon_quote']].dropna()
#dfresult.to_csv('/usr/local/airflow/dags/csh_sladeatendimento_transient/SLA' + str(datetime.datetime.now()) + '.csv', encoding='utf_32', decimal=",")
#gravação do arquivo que seria no datalake , porém foi no arquivo local
dfresult.to_csv('/usr/local/airflow/dags/csh_sladeatendimento_transient/SLA.csv', encoding='utf_32', decimal=",")