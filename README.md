## Projeto Engenharia de Dados - Pipeline de Aluguel de Imóveis 🏠

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Este projeto tem como objetivo criar um pipeline completo de dados para gerenciar, analisar e visualizar informações relacionadas ao aluguel de imóveis. A arquitetura desenvolvida permite desde a extração de dados do nosso banco de origem até o processamento, armazenamento e visualização em dashboards interativos.

O foco principal é oferecer uma solução escalável e eficiente, utilizando ferramentas modernas para integrar grandes volumes de dados, garantindo a confiabilidade, segurança e acessibilidade das informações. O projeto cobre todas as etapas da engenharia de dados: ingestão, transformação, análise e apresentação, com ênfase em boas práticas e tecnologias amplamente utilizadas no mercado.

Entre os casos de uso contemplados, estão:

- **Análise de mercado imobiliário** para identificar tendências de preço e demanda.
- **Monitoramento de locações e contratos** por meio de relatórios dinâmicos.
- **Insights sobre desempenho e ocupação** de imóveis para proprietários e administradoras.

A solução foi desenvolvida pensando em flexibilidade e expansibilidade, permitindo futuras integrações e escalabilidade para lidar com novos cenários e dados.

## Modelo Físico

Utilizamos a ferramenta de modelagem de dados MySQL Workbench para criação do modelo físico do banco de dados, para posterior exportação dos scripts DDL das tabelas e relacionamentos.<br>

![Modelo Físico](https://github.com/user-attachments/assets/2009e741-0fd4-4612-be37-766dabb12cff)


## Dicionário de dados

As informações sobre as tabelas e índices foram documentadas na planilha [template imóvel](https://github.com/marchingbeagle/pipeline-edd/blob/main/docs/dicionario_dados_locadora_im%C3%B3vel.xlsx).

## Começando

Essas instruções permitirão que você obtenha uma cópia do projeto em operação na sua máquina local para fins de desenvolvimento e teste.

Consulte **[Implantação](#-implanta%C3%A7%C3%A3o)** para saber como implantar o projeto.

## Desenho de Arquitetura

Coloque uma imagem do seu projeto, como no exemplo abaixo:

![Desenho de Arquitetura](https://github.com/user-attachments/assets/7c145088-6852-4cad-b004-b6c86e529266)

## 🔧 Pré-requisitos

Para executar o projeto, você precisa ter os seguintes softwares instalados na sua máquina:

- Docker: Ferramenta para criar e gerenciar containers.
- Docker Compose: Ferramenta para definir e rodar aplicações com múltiplos containers.

## 🐳 Configurações Docker  

### **Portainer (Opcional)**  
```bash
docker volume create portainer_data2
docker run -d -p 8000:8000 -p 9443:9443 --name portainer2 --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data2:/data \
  portainer/portainer-ce:2.21.4
```

### **Subir Docker-Compose**  
```bash
docker compose -f docker-compose.yaml up -d
```

### **Criar Usuário no Airflow**  
```bash
docker compose run airflow-webserver airflow users create --role Admin \
  --username airflow --email airflow@example.com \
  --firstname airflow --lastname airflow --password airflow
```

---

## 🌐 Conexões

|        Application        |URL                          |Credentials                         |
|----------------|-------------------------------|-----------------------------|
|Airflow| [http://localhost:8085](http://localhost:8085) | ``` User: airflow``` <br> ``` Pass: airflow``` |         |
|MinIO| [http://localhost:9001](http://localhost:9001) | ``` User: airflow``` <br> ``` Pass: airflowairflow``` |           |
|Postgres| **Server/Database:** localhost:5432/airflow | ``` User: airflow``` <br> ``` Pass: airflow``` |           |
|Spark (Master) | [http://localhost:8081](http://localhost:8081)|  |         |

## Ferramentas utilizadas

As seguintes ferramentas foram utilizadas no projeto:

- [PostgreSQL](https://www.postgresql.org/) - Banco de dados relacional
- [Apache Airflow](https://airflow.apache.org/) - Gerenciador de workflows
- [Apache Spark](https://spark.apache.org/) - Processamento distribuído de dados
- [MinIO](https://min.io/) - Armazenamento de objetos compatível com S3

Ferramentas auxiliares:

- [Python](https://www.python.org/) - Linguagem de programação para desenvolvimento de scripts e análises
- [Docker](https://www.docker.com/) - Containerização para ambientes de desenvolvimento consistentes
- [Delta Lake](https://delta.io/) - Armazenamento de dados transacional para lakes

## Colaboração

Se desejar publicar suas modificações em um repositório remoto no GitHub, siga estes passos:

1. Crie um novo repositório vazio no GitHub.
2. No terminal, navegue até o diretório raiz do projeto.
3. Execute os seguintes comandos:

```bash
git remote set-url origin https://github.com/seu-usuario/nome-do-novo-repositorio.git
git add .
git commit -m "Adicionar minhas modificações"
git push -u origin master
```

Isso configurará o repositório remoto e enviará suas modificações para lá.

## Autores

- **Erik Schneider** - [(https://github.com/marchingbeagle)](https://github.com/marchingbeagle)
- **Gabriel William** - [https://github.com/GabrielWDuarte](https://github.com/GabrielWDuarte)
- **Dauane Neves** - [https://github.com/dauaneneves](https://github.com/dauaneneves)
- **Gabriel Rodrigues** - [https://github.com/gabrieldorodrigues](https://github.com/gabrieldorodrigues)

Você também pode ver a lista de todos os [colaboradores](https://github.com/marchingbeagle/pipeline-edd/graphs/contributors) que participaram deste projeto.

## Licença

Este projeto está sob a licença (sua licença) - veja o arquivo [LICENSE](https://github.com/marchingbeagle/pipeline-edd/blob/main/LICENSE) para detalhes.
