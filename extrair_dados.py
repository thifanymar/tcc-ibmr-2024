# IMPORTANDO AS BIBLIOTECAS A SEREM UTILIZADAS
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd

# INICIANDO A CONEXÃO COM O BANCO
load_dotenv()
database_url = os.getenv('db_url')
engine = create_engine(database_url)

# TABELAS A SEREM EXTRAIDAS DO BANCO
tabelas = ['venda','usuario','equipe','venda_corretor','cliente_venda','cliente_crm','empreendimento','incorporador']

# EXTRAINDO AS TABELAS E SALVANDO EM UM DIRETÓRIO LOCAL EM XLSX
for tabela in tabelas:

    query = f"SELECT * FROM {tabela}"
    df = pd.read_sql(query, con=engine)
    df.to_excel(f'files\{tabela}.xlsx', sheet_name=f'{tabela}', index=False)

engine.dispose()