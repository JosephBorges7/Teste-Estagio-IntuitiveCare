-- 2. CRIAÇÃO DAS TABELAS DEFINITIVAS

-- Tabela de Cadastro das Operadoras
CREATE TABLE operadoras (
    registro_ans VARCHAR(20) PRIMARY KEY,
    cnpj VARCHAR(20),
    razao_social VARCHAR(255),
    modalidade VARCHAR(100),
    uf CHAR(2)
);

-- Tabela de Despesas Consolidadas (Fato)
CREATE TABLE despesas_consolidadas (
    id SERIAL PRIMARY KEY,
    registro_ans VARCHAR(20),
    trimestre INT NOT NULL,
    ano INT NOT NULL,
    valor_despesa DECIMAL(18,2),
    CONSTRAINT fk_operadora FOREIGN KEY (registro_ans) REFERENCES operadoras(registro_ans)
);

-- 3. TABELA DE STAGING (Para evitar o erro de Chave Estrangeira durante o Python)
-- Você carrega o CSV aqui primeiro, depois filtra para a tabela oficial.
CREATE TABLE staging_despesas (
    registro_ans VARCHAR(20),
    trimestre INT,
    ano INT,
    valor_despesa DECIMAL(18,2)
);

-- 4. TABELA PARA RESULTADOS AGREGADOS (Etapa 2.3 do desafio)
CREATE TABLE despesas_agregadas (
    razao_social VARCHAR(255),
    uf CHAR(2),
    total_despesas DECIMAL(18,2),
    media_trimestral DECIMAL(18,2),
    desvio_padrao DECIMAL(18,2),
    PRIMARY KEY (razao_social, uf)
);

-- 5. ÍNDICES PARA PERFORMANCE
-- Otimiza buscas por período e localização
CREATE INDEX idx_despesas_periodo ON despesas_consolidadas (ano, trimestre);
CREATE INDEX idx_operadoras_uf ON operadoras (uf);
CREATE INDEX idx_agregados_razao ON despesas_agregadas (razao_social);