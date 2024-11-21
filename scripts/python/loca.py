from faker import Faker
import pandas as pd

fake = Faker(locale='pt-BR')

idlocacao = []
inquilino = []
valor_contrato = []
vigencia = []
localizacao = []
corretor = []
imovel = []

for i in range(10000):
    idlocacao.append(fake.uuid4())                      
    inquilino.append(fake.name())                      
    valor_contrato.append(fake.random_int(1000, 20000))
    vigencia.append(fake.date_this_year())             
    localizacao.append(fake.address())                 
    corretor.append(fake.name())                       
    imovel.append(fake.uuid4())                        

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
