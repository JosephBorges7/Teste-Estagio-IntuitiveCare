### 🏥 Teste Técnico – Intuitive Care

**Candidato:** Joseph Borges Morais  
**Perfil:** Acadêmico de Bacharelado em Sistemas de Informação – 6º Semestre (IFBA)  
**Foco:** Back-end Development & Data Engineering

---

### 🏗️ Arquitetura do Projeto

O projeto foi estruturado seguindo o modelo de pipeline **ETL (Extract, Transform, Load)**, garantindo a separação de responsabilidades entre a coleta, o tratamento e a persistência dos dados.

---

### 🚀 Guia de Execução (Passo a Passo)

Para garantir a integridade dos dados, siga rigorosamente a ordem abaixo:

#### 1. Preparação do Ambiente

```bash
# Criar o ambiente virtual
python -m venv .venv

# Ativar o ambiente virtual
# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

# Instalar dependências principais
pip install pandas requests beautifulsoup4 sqlalchemy psycopg2-binary
```

---

#### 2. Configuração do Banco de Dados

- Crie um banco de dados PostgreSQL chamado `intuitive_db`.
- Execute o script `schema.sql` para criar tabelas, chaves primárias, chaves estrangeiras e índices.

---

#### 3. Execução do Pipeline ETL

- **Extração:** `python main.py`
- **Tratamento:** `python transformacao.py`
- **Enriquecimento:** `python enriquecimento.py`
- **Inteligência:** `python agregacao.py`

---

#### 4. Carga de Dados (Load)

Execute:
```bash
python importacao.py
```

---

#### 5. Validação e Análise

Execute as queries contidas em `analise.sql` no cliente SQL (ex: pgAdmin).

---

### 🧠 Decisões de Engenharia e Trade-offs

#### Processamento e Memória
Processamento incremental para evitar erros de **Out of Memory (OOM)**.

#### Modelagem de Dados
Uso de tabelas normalizadas com **Foreign Keys**.

#### Precisão Financeira
Uso de `DECIMAL(18,2)` para garantir exatidão.

---

### 📊 SQL Analytics

```sql
((valor_periodo_atual - valor_periodo_anterior) 
 / valor_periodo_anterior) * 100
```

---

### 📂 Estrutura de Arquivos

- `saida/`
- `schema.sql`
- `importacao.py`

