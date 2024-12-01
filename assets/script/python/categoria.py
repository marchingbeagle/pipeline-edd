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

for i in range(10000):
    idcategoria.append(fake.random.randint(1, 99999))
    nome.append(fake.random.choice(['alugado', 'reservado', 'disponível']))    
    descricao.append(fake.text(max_nb_chars=30))  
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

df.to_csv('./CATEGORIA.CSV', index=False)
