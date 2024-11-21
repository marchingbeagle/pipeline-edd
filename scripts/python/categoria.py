from faker import Faker
import pandas as pd
from datetime import datetime, timedelta

fake = Faker(locale='pt-BR')

idcategoria = []
nome = []
descricao = []
data_criacao = [] 
data_atualizacao = []

def random_date_within_3_years():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3 * 365)
    return fake.date_between(start_date=start_date, end_date=end_date)

for i in range(5):
    idcategoria.append(fake.uuid4()) 
    nome.append(fake.word())          
    descricao.append(fake.text(max_nb_chars=50))  
    data_criacao.append(random_date_within_3_years()) 
    data_atualizacao.append(random_date_within_3_years())  

df = pd.DataFrame(
    {
        'idcategoria': idcategoria,
        'nome': nome,
        'descricao': descricao,
        'data_criacao': data_criacao,
        'data_atualizacao': data_atualizacao,
    }
)

print(df)

#df.to_csv('./CATEGORIA.CSV', index=False)
