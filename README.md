# 🏥 Teste de Integração - Dados Abertos ANS
> **Candidato:** Joseph Borges Morais  
> **Objetivo:** Automatização do pipeline ETL para extração e consolidação de Demonstrações Contábeis da ANS.

[cite_start]Este projeto realiza o consumo da API de Dados Abertos da ANS [cite: 26][cite_start], processa arquivos de grandes volumes de forma resiliente e consolida dados financeiros[cite: 41].

---

## 🚀 Como Executar o Projeto
[cite_start]O projeto foi desenvolvido em **Python**[cite: 12].

1. **Configuração do Ambiente:**
   ```bash
   # Criar e ativar o ambiente virtual
   python -m venv .venv
   source .venv/Scripts/activate  # No Git Bash
   
   # Instalar dependências
   pip install pandas requests beautifulsoup4 openpyxl

2. **Execução:**
    ```bash 
   python main.py

   ---

### Parte 2: Justificativas Técnicas (Trade-offs)
Este trecho atende aos pontos onde o teste pede para "Documentar sua escolha e justificar".

```markdown
---

## 🧠 Decisões Técnicas e Trade-offs 

### 1. Processamento Incremental vs. Memória (Requisito 1.2) 
* **Decisão:** Processamento **Incremental**.
* **Justificativa:** Dado que os arquivos da ANS podem conter milhões de registros por trimestre, o carregamento total em memória apresentaria risco de *Out of Memory*. O processamento incremental garante que o consumo de RAM permaneça baixo e constante, independentemente do volume de dados.

### 2. Resiliência de Estrutura (Requisito 1.1) 
* **Decisão:** Navegação dinâmica via Web Scraping.
* **Justificativa:** A estrutura de diretórios da ANS pode variar. O script utiliza `BeautifulSoup` para identificar os links reais de anos e trimestres no servidor FTP, tornando-o resiliente a mudanças de layout na fonte.

---

## [cite_start]🔍 Análise Crítica de Inconsistências (Requisito 1.3) 

| [cite_start]Inconsistência  | [cite_start]Abordagem | [cite_start]Justificativa  |
| :--- | :--- | :--- |
| [cite_start]**CNPJs Duplicados**  | `keep='last'` | [cite_start]Prioriza a Razão Social mais recente, assumindo atualização cadastral. |
| [cite_start]**Valores Negativos** | **Manter/Corrigir** | [cite_start]Mantidos para preservar a integridade contábil (provisões/estornos). |
| [cite_start]**Datas Inconsistentes**  | **Extração via Regex** | [cite_start]Extração direta do nome do diretório/arquivo para garantir padronização. |



---

## 📂 Entrega Final
O arquivo consolidado está localizado em `saida/consolidado_despesas.zip`, contendo as colunas: `CNPJ`, `RazaoSocial`, `Trimestre`, `Ano` e `ValorDespesas`.