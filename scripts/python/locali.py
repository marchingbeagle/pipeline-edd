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
    idlocalizacao.append(fake.random.randint(1, 99999))           
    cep.append(fake.postcode())                  
    numero_imovel.append(fake.random.randint(1, 9999))
    complemento.append(fake.random_element(['Apto', 'Casa', 'Bloco', 'Edifício'])) 
    referencia.append(fake.sentence(nb_words=2))
    cidade.append(fake.city())                 
    categoria.append(fake.random.choice(['alugado', 'reservado', 'disponível']))             

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
