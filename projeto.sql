CREATE TABLE Estrategia (
  id_estrategia INT PRIMARY KEY,
  nome VARCHAR,
  descricao VARCHAR,
  publico_alvo VARCHAR,
  tom_voz VARCHAR,
  objetivos VARCHAR,
  data_criacao DATE
);

CREATE TABLE Usuario (
  id_usuario INT PRIMARY KEY,
  nome VARCHAR,
  email VARCHAR UNIQUE,
  senha VARCHAR,
  perfil VARCHAR,
  data_criacao DATE
);

CREATE TABLE Metrica (
  id_metrica INT PRIMARY KEY,
  alcance VARCHAR,
  engajamento VARCHAR,
  taxa_conversao VARCHAR,
  id_usuario INT,
  id_estrategia INT,
  FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
  FOREIGN KEY (id_estrategia) REFERENCES Estrategia(id_estrategia)
);

CREATE TABLE Conteudo (
  id_conteudo INT PRIMARY KEY,
  titulo VARCHAR,
  corpo VARCHAR,
  status VARCHAR,
  data_criacao DATE,
  data_publicacao DATE,
  id_usuario INT,
  id_estrategia INT,
  FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
  FOREIGN KEY (id_estrategia) REFERENCES Estrategia(id_estrategia)
);

CREATE TABLE Prompt (
  id_prompt INT PRIMARY KEY,
  conteudo_prompt VARCHAR,
  contexto VARCHAR,
  resultado_gerado VARCHAR,
  data_execucao DATE,
  id_conteudo INT,
  id_usuario INT,
  FOREIGN KEY (id_conteudo) REFERENCES Conteudo(id_conteudo),
  FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

CREATE TABLE Log_Validacao (
  id_log INT PRIMARY KEY,
  resultado_validacao VARCHAR,
  erros_detectados VARCHAR,
  data_validacao DATE,
  id_usuario INT,
  FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

CREATE TABLE Tendencias (
  id_tendencia INT PRIMARY KEY,
  palavra_chave VARCHAR,
  descricao VARCHAR,
  frequencia VARCHAR,
  origem VARCHAR,
  data_registro DATE,
  id_usuario INT,
  FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);