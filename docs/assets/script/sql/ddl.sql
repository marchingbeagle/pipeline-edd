CREATE SCHEMA IF NOT EXISTS mydb;

CREATE TABLE IF NOT EXISTS mydb.pessoas (
  idpessoas SERIAL PRIMARY KEY,
  nome VARCHAR(45) NOT NULL,
  cpf VARCHAR(11) NOT NULL,
  data_nascimento TIMESTAMPTZ NOT NULL,
  endereco VARCHAR(45) NOT NULL,
  telefone VARCHAR(45) NOT NULL,
  sexo VARCHAR(45) NOT NULL
);

CREATE TABLE IF NOT EXISTS mydb.log (
  idlog SERIAL PRIMARY KEY,
  titulo VARCHAR(45) NOT NULL,
  descricao TEXT NOT NULL,
  data TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS mydb.estado (
  idestado SERIAL PRIMARY KEY,
  nome_estado VARCHAR(45) NOT NULL,
  sigla_estado VARCHAR(2) NOT NULL
);

CREATE TABLE IF NOT EXISTS mydb.cidade (
  idcidade SERIAL PRIMARY KEY,
  nome VARCHAR(45) NOT NULL,
  estado INT NOT NULL,
  CONSTRAINT fk_estado FOREIGN KEY (estado)
    REFERENCES mydb.estado (idestado)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS mydb.categoria (
  idcategoria SERIAL PRIMARY KEY,
  nome VARCHAR(45) NULL,
  descricao VARCHAR(45) NULL,
  data_criacao TIMESTAMPTZ NULL,
  data_atualizacao TIMESTAMPTZ NULL
);

CREATE TABLE IF NOT EXISTS mydb.localizacao (
  idlocalizacao SERIAL PRIMARY KEY,
  cep VARCHAR(8) NOT NULL,
  numero_imovel VARCHAR(10) NOT NULL,
  complemento VARCHAR(45) NULL,
  referencia VARCHAR(45) NULL,
  cidade INT NULL,
  categoria INT NULL,
  CONSTRAINT fk_cidade FOREIGN KEY (cidade)
    REFERENCES mydb.cidade (idcidade)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_categoria FOREIGN KEY (categoria)
    REFERENCES mydb.categoria (idcategoria)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS mydb.imovel (
  idimovel SERIAL PRIMARY KEY,
  localizacao INT NULL,
  proprietario INT NULL,
  preco_compra INT NULL,
  preco_aluguel INT NULL,
  CONSTRAINT fk_localizacao FOREIGN KEY (localizacao)
    REFERENCES mydb.localizacao (idlocalizacao)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_proprietario FOREIGN KEY (proprietario)
    REFERENCES mydb.pessoas (idpessoas)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS mydb.locacao (
  idlocacao SERIAL PRIMARY KEY,
  inquilino INT NOT NULL,
  valor_contrato INT NOT NULL,
  vigencia TIMESTAMPTZ NOT NULL,
  localizacao INT NOT NULL,
  corretor INT NOT NULL,
  imovel INT NOT NULL,
  CONSTRAINT fk_inquilino FOREIGN KEY (inquilino)
    REFERENCES mydb.pessoas (idpessoas)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_imovel FOREIGN KEY (imovel)
    REFERENCES mydb.imovel (idimovel)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);
