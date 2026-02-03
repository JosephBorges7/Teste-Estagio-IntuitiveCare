import os
import pandas as pd
from sqlalchemy import create_engine, text

# =========================
# CONFIGURAÇÕES (AJUSTE CONFORME SEU AMBIENTE)
# =========================
DB_URL = "postgresql://postgres:SUASENHA@localhost:5432/intuitive_db"
PASTA_SAIDA = "saida"

ARQUIVO_OPERADORAS = "Relatorio_cadop.csv"
ARQUIVO_DESPESAS = "consolidado_despesas.csv"
ARQUIVO_AGREGADOS = "despesas_agregadas.csv"


# =========================
# FUNÇÕES AUXILIARES
# =========================
def criar_engine():
    return create_engine(DB_URL)


def normalizar_colunas(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.upper()
        .str.replace(" ", "_")
    )
    return df


def converter_decimal(serie):
    return (
        pd.to_numeric(
            serie.astype(str).str.replace(",", "."),
            errors="coerce"
        )
        .fillna(0)
    )


def limpar_tabelas(engine):
    with engine.begin() as conn:
        print("🧹 Limpando dados antigos...")
        conn.execute(
            text(
                "TRUNCATE TABLE "
                "despesas_agregadas, despesas_consolidadas, operadoras CASCADE;"
            )
        )


# =========================
# IMPORTAÇÕES
# =========================
def importar_operadoras(engine):
    print("📥 Importando operadoras...")

    df = pd.read_csv(ARQUIVO_OPERADORAS, sep=";", encoding="utf-8-sig")
    df = normalizar_colunas(df)

    col_registro = (
        "REGISTRO_OPERADORA"
        if "REGISTRO_OPERADORA" in df.columns
        else "REGISTRO_ANS"
    )

    col_razao_social = (
        "RAZAO_SOCIAL"
        if "RAZAO_SOCIAL" in df.columns
        else df.columns[2]
    )

    operadoras = pd.DataFrame({
        "registro_ans": df[col_registro].astype(str).str.zfill(6),
        "cnpj": df["CNPJ"].astype(str),
        "razao_social": df[col_razao_social].fillna("NOME NÃO INFORMADO"),
        "modalidade": df.get("MODALIDADE", "NÃO INFORMADA"),
        "uf": df.get("UF", "ND")
    })

    operadoras.to_sql("operadoras", engine, if_exists="append", index=False)
    print("   ✅ Tabela 'operadoras' populada.")


def importar_despesas(engine):
    print("📥 Importando despesas consolidadas...")

    caminho = os.path.join(PASTA_SAIDA, ARQUIVO_DESPESAS)
    df = pd.read_csv(caminho, sep=";", encoding="utf-8-sig")
    df = normalizar_colunas(df)

    despesas = pd.DataFrame({
        "registro_ans": df["CNPJ"].astype(str).str.zfill(6),
        "trimestre": pd.to_numeric(df["TRIMESTRE"], errors="coerce").fillna(0).astype(int),
        "ano": pd.to_numeric(df["ANO"], errors="coerce").fillna(0).astype(int),
        "valor_despesa": converter_decimal(df["VALORDESPESAS"])
    })

    despesas.to_sql(
        "despesas_consolidadas",
        engine,
        if_exists="append",
        index=False
    )

    print("   ✅ Tabela 'despesas_consolidadas' populada.")


def importar_agregados(engine):
    print("📥 Importando despesas agregadas...")

    caminho = os.path.join(PASTA_SAIDA, ARQUIVO_AGREGADOS)

    if not os.path.exists(caminho):
        print("   ⚠️ Arquivo 'despesas_agregadas.csv' não encontrado.")
        return

    df = pd.read_csv(caminho, sep=";", encoding="utf-8-sig")
    df = normalizar_colunas(df)

    agregados = pd.DataFrame({
        "razao_social": df["RAZAOSOCIAL"].fillna("NOME NÃO INFORMADO"),
        "uf": df["UF"].fillna("ND"),
        "total_despesas": converter_decimal(df["TOTALDESPESAS"]),
        "media_trimestral": converter_decimal(df["MEDIATRIMESTRAL"]),
        "desvio_padrao": converter_decimal(df["DESVIOPADRAODESPESAS"])
    })

    agregados.to_sql(
        "despesas_agregadas",
        engine,
        if_exists="append",
        index=False
    )

    print("   ✅ Tabela 'despesas_agregadas' populada.")


# =========================
# EXECUÇÃO PRINCIPAL
# =========================
def executar_importacao():
    print("🚀 Iniciando Carga de Dados no Banco ...")

    engine = criar_engine()

    try:
        limpar_tabelas(engine)
        importar_operadoras(engine)
        importar_despesas(engine)
        importar_agregados(engine)

        print("🎉 Importação finalizada com sucesso!")

    except Exception as erro:
        print(f"❌ Erro durante a importação: {erro}")


if __name__ == "__main__":
    executar_importacao()