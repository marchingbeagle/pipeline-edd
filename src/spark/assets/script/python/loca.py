from faker import Faker
import pandas as pd
from datetime import datetime, timedelta

fake = Faker(locale='pt-BR')

idlocacao = []
inquilino = []
valor_contrato = []
vigencia = []
localizacao = []
corretor = []
imovel = []

def random_date_within_3_years():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3 * 365)
    return fake.date_between(start_date=start_date, end_date=end_date)

for i in range(10000):
    idlocacao.append(fake.random.randint(1, 99999))                      
    inquilino.append(fake.name())                      
    valor_contrato.append(fake.random_int(1000, 20000))
    vigencia.append(random_date_within_3_years())             
    localizacao.append(fake.address())                 
    corretor.append(fake.name())                       
    imovel.append(fake.random.randint(1, 99999))                       

df = pd.DataFrame(
    {
        'idlocacao': idlocacao,
        'inquilino': inquilino,
        'valor_contrato': valor_contrato,
        'vigencia': vigencia,
        'localizacao': localizacao,
        'corretor': corretor,
        'imovel': imovel,
    }
)

print(df)
df.to_csv('./LOCACAO.CSV', index=False)
