from faker import Faker
import pandas as pd

fake = Faker(locale='pt-BR')

idestado = []
nome_estado = []
sigla_estado = []

for i in range(10000):
    idestado.append(fake.uuid4())                    
    nome_estado.append(fake.state())                
    sigla_estado.append(fake.state_abbr())          

df = pd.DataFrame(
    {
        'idestado': idestado,
        'nome_estado': nome_estado,
        'sigla_estado': sigla_estado,
    }
)

print(df)
df.to_csv('./ESTADO.CSV', index=False)
