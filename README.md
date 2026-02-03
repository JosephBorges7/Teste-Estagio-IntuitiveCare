
---

"### 🏥 Teste Técnico - (Intuitive Care)"
"**Candidato:**" Joseph Borges Morais
"**Perfil:**" Acadêmico de Bacharelado em Sistemas de Informação - 6º Semestre (IFBA)
"**Foco:**" Back-end Development & Data Engineering

---

"### 🏗️ Arquitetura do Projeto"
O projeto foi estruturado seguindo o modelo de pipeline `"**ETL (Extract, Transform, Load)**"`, garantindo a separação de responsabilidades entre a coleta, o tratamento e a persistência dos dados.

---

"### 🚀 Guia de Execução (Passo a Passo)"

Para garantir a integridade dos dados, siga a ordem rigorosa abaixo:

"**1. Preparação do Ambiente:**"

```bash
"**# Criar e ativar o ambiente virtual**"
python -m venv .venv
source .venv/Scripts/activate 

"**# Instalar dependências core**"
pip install pandas requests beautifulsoup4 sqlalchemy psycopg2-binary

```

"**2. Configuração do Banco de Dados:**"

* Crie um banco de dados no PostgreSQL chamado `intuitive_db`.
* Execute o script `"**schema.sql**"` para estruturar as tabelas, chaves primárias e índices.

"**3. Execução do Pipeline ETL:**"

* `"**Extração:**"` `python main.py` (Download e extração via Web Scraping resiliente).
* `"**Tratamento:**"` `python transformacao.py` (Limpeza e padronização inicial).
* `"**Enriquecimento:**"` `python enriquecimento.py` (Cruzamento de dados entre operadoras e despesas).
* `"**Inteligência:**"` `python agregacao.py` (Geração do arquivo de KPIs estatísticos).

"**4. Carga de Dados (Data Loading):**"

* Execute `python importacao.py` para realizar a ingestão automatizada dos arquivos CSV para o PostgreSQL. Este script trata inconsistências de tipos e valores nulos em tempo real.

"**5. Validação e Análise:**"

* Execute as queries contidas em `"**analise.sql**"` no seu cliente SQL (pgAdmin) para extrair os relatórios de crescimento e Market Share.

---

"### 🧠 Decisões de Engenharia e Trade-offs"

"#### 1. Processamento e Memória (Etapa 1.2)"

* "**Estratégia:**" Processamento Incremental por arquivos.
* "**Justificativa:**" Para suportar o volume massivo da ANS (centenas de milhares de linhas por trimestre), evitamos o carregamento em lote na RAM, prevenindo erros de `"**Stack Overflow**"` ou `"**Out of Memory**"`.

"#### 2. Modelagem de Dados (Etapa 3.2)"

* "**Abordagem:**" `"**Opção B (Tabelas Normalizadas)**"`.
* "**Justificativa:**"
* `"**Escalabilidade:**"` Reduz a redundância de dados cadastrais (Razão Social, UF) que se repetem milhões de vezes nas despesas.
* `"**Integridade:**"` Uso de `"**Foreign Keys (FK)**"` para garantir que nenhuma despesa seja órfã de uma operadora cadastrada.



"#### 3. Precisão Financeira (Etapa 3.2)"

* "**Tipo de Dado:**" `"**DECIMAL(18,2)**"`.
* "**Justificativa:**" Em sistemas de back-end contábil, o uso de `FLOAT` é evitado devido à imprecisão binária em grandes somas. O `DECIMAL` garante que cálculos de bilhões de reais sejam exatos.

---

"### 🔍 Qualidade e Higiene de Dados (Etapa 1.3 & 3.3)"

Para garantir a confiabilidade dos relatórios, implementei:

* `"**Regex Sanitization:**"` Extração de metadados diretamente dos nomes dos arquivos para evitar erros de digitação nas planilhas.
* `"**Normalização de Tipos:**"` Conversão automática de strings/vírgulas em formatos numéricos compatíveis com o PostgreSQL durante a importação.
* `"**Deduplicação Inteligente:**"` Lógica de `"**keep last**"` para manter apenas a versão mais atualizada da razão social de cada operadora.

---

"### 📊 SQL Analytics (Fórmulas de Negócio)"
O sistema utiliza a seguinte lógica para o cálculo de crescimento percentual entre períodos:

---

"### 📂 Estrutura de Arquivos"

* `"**saida/**"`: Artefatos gerados (CSVs e ZIPs consolidados).
* `"**schema.sql**"`: Definição de tabelas, PKs, FKs e Índices de performance.
* `"**importacao.py**"`: Script de carga com tratamento de exceções e normalização de headers.

---


