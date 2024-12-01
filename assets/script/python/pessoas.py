from faker import Faker
import pandas as pd

fake = Faker(locale='pt-BR')

idpessoas = []
nome = []
cpf = []
data_nascimento = []
endereco = []
telefone = []
sexo = []

for i in range(10000):
    idpessoas.append(fake.random.randint(1, 99999)) 
    nome.append(fake.name())        
    cpf.append(fake.cpf())          
    data_nascimento.append(fake.date_of_birth())  
    endereco.append(fake.street_address())        
    telefone.append(fake.phone_number())          
    sexo.append(fake.random_element(['M', 'F']))  

df = pd.DataFrame(
    {
        'idpessoas': idpessoas,
        'nome': nome,
        'cpf': cpf,
        'data_nascimento': data_nascimento,
        'endereco': endereco,
        'telefone': telefone,
        'sexo': sexo,
    }
)

print(df)
df.to_csv('./PESSOAS.CSV', index=False)
