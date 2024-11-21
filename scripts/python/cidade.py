from faker import Faker
import pandas as pd

fake = Faker(locale='pt-BR')

idcidade = []
nome = []
estado = []

for i in range(10000):
    idcidade.append(fake.uuid4())       
    nome.append(fake.city())            
    estado.append(fake.state())         

df = pd.DataFrame(
    {
        'idcidade': idcidade,
        'nome': nome,
        'estado': estado,
    }
)

print(df)
df.to_csv('./CIDADE.CSV', index=False)
