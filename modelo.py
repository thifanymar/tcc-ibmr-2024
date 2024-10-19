import pandas as pd
import numpy as np
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

# lendo os arquivos 
df_venda = pd.read_excel(r'files\venda.xlsx')
df_usuario = pd.read_excel(r'files\usuario.xlsx')
df_corretor_venda = pd.read_excel(r'files\corretor_venda.xlsx')
df_equipe = pd.read_excel(r'files\equipe.xlsx')
df_cliente_crm = pd.read_excel(r'files\cliente_crm.xlsx')
df_cliente_venda = pd.read_excel(r'files\cliente_venda.xlsx')
df_incorporador = pd.read_excel(r'files\incorporador.xlsx')
df_empreendimento = pd.read_excel(r'files\empreendimento.xlsx')


# TODO: colocar tudo em string menos data e valor de venda, fgts, renda, financiamento
colunas = ['num_venda','num_empreendimento']
df_venda[colunas] = df_venda[colunas].astype(str)

colunas = ['num_usuario', 'nome_usuario', 'cpf_usuario']
df_usuario[colunas] = df_usuario[colunas].astype(str)

colunas = ['num_venda', 'num_corretor', 'num_equipe']
df_corretor_venda[colunas] = df_corretor_venda[colunas].astype(str)

colunas = ['num_equipe', 'num_gerente', 'num_diretor']
df_equipe[colunas] = df_equipe[colunas].astype(str)

colunas = ['num_cliente', 'nome', 'bairro', 'cep', 'profissao', 'escolaridade','uf', 'estado_civil']
df_cliente_crm[colunas] = df_cliente_crm[colunas].astype(str)

colunas = ['num_cliente','num_venda']
df_cliente_venda[colunas] = df_cliente_venda[colunas].astype(str)

colunas = ['num_incorporador', 'nome_incorporador']
df_incorporador[colunas] = df_incorporador[colunas].astype(str)

colunas = ['num_empreendimento', 'num_incorporador', 'nome_empreendimeto','cep_empreendimento', 'bairro_empreendimento', 'uf_empreendimento']
df_empreendimento[colunas] = df_empreendimento[colunas].astype(str)

# montar tabela fato venda
fVenda = pd.merge(df_venda,df_corretor_venda,how='right',left_on='num_venda',right_on='num_venda')
fVenda = fVenda.drop(columns=['num_corretor'])
fVenda = pd.merge(fVenda,df_cliente_venda,how='right',left_on='num_venda',right_on='num_venda')
fVenda = fVenda.drop(columns=['valor_fgts','valor_renda','valor_financiamento'])
# montar tabela cliente
dCliente = pd.merge(df_cliente_crm,df_cliente_venda,how='right',left_on='num_cliente',right_on='num_cliente')

# montar tabela equipe

df_usuario_gerente = df_usuario.copy()
df_usuario_gerente = df_usuario_gerente.rename({'num_usuario':'num_gerente',
                                                'nome_usuario':'nome_gerente',
                                                'cpf_usuario':'cpf_gerente',
                                                'data_nascimento':'data_nascimento_gerente',
                                                }, axis='columns')

df_usuario_diretor = df_usuario.copy()
df_usuario_diretor = df_usuario_diretor.rename({'num_usuario':'num_diretor',
                                                'nome_usuario':'nome_diretor',
                                                'cpf_usuario':'cpf_diretor',
                                                'data_nascimento':'data_nascimento_diretor',
                                                }, axis='columns')

dEquipe = pd.merge(df_equipe,df_usuario_gerente,how='left',left_on='num_gerente',right_on='num_gerente')
dEquipe = pd.merge(dEquipe,df_usuario_diretor,how='left',left_on='num_diretor',right_on='num_diretor')

dEquipe = dEquipe.drop(columns=['data_nascimento_gerente',
                                'cpf_gerente',
                                'data_nascimento_diretor',
                                'cpf_diretor'])

# montar tabela produto
dProduto = pd.merge(df_empreendimento,df_incorporador,how='left',left_on='num_incorporador',right_on='num_incorporador')

# montar tabela calendario

dCalendario = ''
data_inicio = '2024-01-01'
data_fim = '2024-12-31'

datas = pd.date_range(start=data_inicio, end=data_fim, freq='D')
# Criar o DataFrame com as colunas desejadas
dCalendario = pd.DataFrame({
    'data': datas,
    'ano': datas.year,
    'mes': datas.month,
    'dia': datas.day,
    'nome_dia_da_semana': datas.strftime('%A'),
    'nome_mes': datas.strftime('%B'),
})

print(dCalendario)


load_dotenv()
database_url = os.getenv('db_url')
engine = create_engine(database_url)

fVenda.to_sql('fvenda', con=engine, if_exists='replace', index=False)
dEquipe.to_sql('dequipe', con=engine, if_exists='replace', index=False)
dProduto.to_sql('dproduto', con=engine, if_exists='replace', index=False)
dCliente.to_sql('dcliente', con=engine, if_exists='replace', index=False)
dCalendario.to_sql('dcalendario', con=engine, if_exists='replace', index=False)

engine.dispose()

# salvar os dados em um banco de dados
