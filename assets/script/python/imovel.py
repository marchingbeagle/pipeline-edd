from faker import Faker
import pandas as pd

fake = Faker(locale='pt-BR')

idimovel = []
localizacao = []
proprietario = []
preco_compra = []
preco_aluguel = []

for i in range(10000):
    idimovel.append(fake.random.randint(1, 99999))                
    localizacao.append(fake.address())             
    proprietario.append(fake.name())               
    preco_compra.append(fake.random_int(50000, 1000000))
    preco_aluguel.append(fake.random_int(500, 5000))    
    
df = pd.DataFrame(
    {
        'idimovel': idimovel,
        'localizacao': localizacao,
        'proprietario': proprietario,
        'preco_compra': preco_compra,
        'preco_aluguel': preco_aluguel,
    }
)

print(df)
df.to_csv('./IMOVEL.CSV', index=False)
