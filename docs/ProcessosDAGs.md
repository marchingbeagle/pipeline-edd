# Landing to Bronze

Este trecho de código define os schemas (estruturas) das tabelas para o processo ETL **landing-to-bronze**.

### Principais aspectos:

Define 7 tabelas principais: **estado**, **cidade**, **categoria**, **localizacao**, **imovel**, **locacao**.  
Cada tabela tem seus campos fortemente tipados.

Este schema serve como base para validação e estruturação dos dados quando são movidos da camada landing para bronze, garantindo integridade e consistência dos dados.

### Principais recursos:
- **Aplicação de tipo de dados**
- **Tratamento de valor nulo**
- **Padronização de texto**
- **Validação de campo obrigatória**
- **Rastreamento de linhagem**
- **Verificações de consistência de esquema**

Isso garante a qualidade e a consistência dos dados ao passar da camada de destino para a camada bronze.

---

# Bronze to Silver

Este código implementa o processo ETL da camada bronze para silver, realizando transformações e enriquecimentos nos dados.

### Principais Funções:

1. **Funções de Limpeza**:
   - `clean_cpf()`: Remove caracteres não numéricos do CPF
   - `clean_phone()`: Padroniza formato do telefone
   - `validate_date()`: Valida e converte campos de data

2. **Processamento por Tabela**:
   - `process_pessoas()`:    
     - Remove duplicatas por CPF
     - Limpa CPF e telefone
     - Padroniza nome em maiúsculo
     - Valida data de nascimento
   - `process_locacao()`:
     - Enriquece dados com joins em imovel e pessoas
     - Filtra contratos com valor válido
     - Valida data de vigência
   - `process_imovel()`:
     - Join com localizacao
     - Valida preços de compra e aluguel

### Principais recursos:
- **Limpeza e padronização de dados**
- **Remoção de duplicatas**
- **Validação de regras de negócio**
- **Enriquecimento via joins**
- **Rastreamento com metadados**
- **Tratamento de erros**
- **Validações específicas por domínio**

Isso garante que os dados na camada silver estejam limpos, enriquecidos e prontos para análise, seguindo regras de negócio específicas para cada domínio.

---

# Silver to Gold

Este trecho de código implementa a execução principal do processo ETL da camada silver para gold, realizando a criação do modelo dimensional e views analíticas.

### Principais aspectos:
Define 3 etapas principais de processamento:
1. **Criação das dimensões e fatos**
2. **Persistência das tabelas dimensionais**
3. **Geração de views analíticas e KPIs**

### Fluxo de execução:
1. Cria tabelas dimensionais:
   - `dim_localizacao`
   - `dim_pessoas`
2. Cria tabela fato:
   - `fact_locacao`
3. Persiste em formato Delta:
   - Salva dimensões
   - Salva fatos
4. Gera views analíticas
5. Gera KPIs

### Principais recursos:
- **Tratamento de exceções**
- **Gerenciamento de sessão Spark**
- **Persistência em Delta Lake**
- **Logging de execução**
- **Cleanup automático de recursos**

Isso garante:
- **Execução confiável do processo**
- **Rastreabilidade de erros**
- **Gestão adequada de recursos**
- **Consistência dos dados na camada gold**
- **Disponibilidade para consumo em dashboards**
