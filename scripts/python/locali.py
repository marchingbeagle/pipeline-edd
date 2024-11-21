from faker import Faker
import pandas as pd

fake = Faker(locale='pt-BR')

idlocalizacao = []
cep = []
numero_imovel = []
complemento = []
referencia = []
cidade = []
categoria = []

for i in range(10000):
    idlocalizacao.append(fake.uuid4())            
    cep.append(fake.postcode())                  
    numero_imovel.append(fake.building_number()) 
    complemento.append(fake.random_element(['Apto', 'Casa', 'Bloco', 'Edifício'])) 
    referencia.append(fake.sentence(nb_words=6))
    cidade.append(fake.city())                 
    categoria.append(fake.word())             

df = pd.DataFrame(
    {
        'idlocalizacao': idlocalizacao,
        'cep': cep,
        'numero_imovel': numero_imovel,
        'complemento': complemento,
        'referencia': referencia,
        'cidade': cidade,
        'categoria': categoria,
    }
)

print(df)
df.to_csv('./LOCALIZACAO.CSV', index=False)
