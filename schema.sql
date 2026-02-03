-- Criação da Tabela de Cadastro das Operadoras
CREATE TABLE operadoras (
    registro_ans VARCHAR(20) PRIMARY KEY,
    cnpj VARCHAR(20),
    razao_social VARCHAR(255),
    modalidade VARCHAR(100),
    uf CHAR(2)
);

-- Criação da Tabela de Despesas Consolidadas
CREATE TABLE despesas_consolidadas (
    id SERIAL PRIMARY KEY,
    registro_ans VARCHAR(20),
    trimestre INT,
    ano INT,
    valor_despesa DECIMAL(18,2),
    CONSTRAINT fk_operadora FOREIGN KEY (registro_ans) REFERENCES operadoras(registro_ans)
);

-- Tabela para dados agregados (Resultados da Etapa 2.3)
CREATE TABLE despesas_agregadas (
    razao_social VARCHAR(255),
    uf CHAR(2),
    total_despesas DECIMAL(18,2),
    media_trimestral DECIMAL(18,2),
    desvio_padrao DECIMAL(18,2),
    PRIMARY KEY (razao_social, uf)
);

-- Índices para Performance em Queries Analíticas 
CREATE INDEX idx_despesas_periodo ON despesas_consolidadas (ano, trimestre);
CREATE INDEX idx_operadoras_uf ON operadoras (uf);

-- Índice extra para busca por Razão Social (frequente em buscas de usuários)
CREATE INDEX idx_agregados_razao ON despesas_agregadas (razao_social);