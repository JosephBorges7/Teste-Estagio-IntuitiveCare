import pandas as pd
import os

def executar_enriquecimento():
    print("🧬 Iniciando Enriquecimento de Dados ...")
    
    caminho_consolidado = os.path.join("saida", "consolidado_validado.csv")
    arquivo_cadastral = "Relatorio_cadop.csv" 

    if not os.path.exists(caminho_consolidado):
        print("❌ Erro: Arquivo consolidado não encontrado!")
        return

    # 1. Carrega dados de despesas (Chave: CNPJ que contém o Registro ANS)
    df_despesas = pd.read_csv(caminho_consolidado, sep=';')
    df_despesas['Key_ANS'] = df_despesas['CNPJ'].astype(str).str.zfill(6)

    # 2. Carrega cadastro ANS (Chave: REGISTRO_OPERADORA)
    try:
        # Usamos sep=';' e latin-1 conforme padrão da ANS
        df_cadastral = pd.read_csv(arquivo_cadastral, sep=';', encoding='utf-8-sig')
        df_cadastral.columns = [c.strip().upper() for c in df_cadastral.columns]
        
        # Padroniza a chave do cadastro para string com 6 dígitos
        df_cadastral['REGISTRO_OPERADORA'] = df_cadastral['REGISTRO_OPERADORA'].astype(str).str.zfill(6)
    except Exception as e:
        print(f"❌ Erro ao ler cadastro: {e}")
        return

    # 3. Executa o JOIN (Requisito 2.2)
    # Uso suffixes para identificar de onde veio cada coluna após o merge
    df_final = pd.merge(
        df_despesas, 
        df_cadastral[['REGISTRO_OPERADORA', 'CNPJ', 'MODALIDADE', 'UF']], 
        left_on='Key_ANS', 
        right_on='REGISTRO_OPERADORA', 
        how='left',
        suffixes=('_despesa', '_cadastro')
    )

    # 4. Organização das Colunas (Requisito 2.2)
    # CNPJ agora deve ser o real (14 dígitos) que veio do cadastro (_cadastro)
    df_saida = pd.DataFrame()
    df_saida['CNPJ'] = df_final['CNPJ_cadastro']
    df_saida['RazaoSocial'] = df_final['RazaoSocial']
    df_saida['Trimestre'] = df_final['Trimestre']
    df_saida['Ano'] = df_final['Ano']
    df_saida['ValorDespesas'] = df_final['ValorDespesas']
    df_saida['RegistroANS'] = df_final['REGISTRO_OPERADORA']
    df_saida['Modalidade'] = df_final['MODALIDADE']
    df_saida['UF'] = df_final['UF']

    # 5. Tratamento de Inconsistências (Requisito 2.2 e Análise Crítica)
    # Caso não encontre o CNPJ no cadastro, mantenho o ID de 6 dígitos original para não perder o dado
    df_saida['CNPJ'] = df_saida['CNPJ'].fillna(df_final['CNPJ_despesa'])

    caminho_saida = os.path.join("saida", "consolidado_enriquecido.csv")
    df_saida.to_csv(caminho_saida, index=False, sep=';', encoding='utf-8-sig')
    print(f"✅ Sucesso! Dados enriquecidos com RegistroANS, Modalidade e UF.")

if __name__ == "__main__":
    executar_enriquecimento()