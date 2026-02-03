import pandas as pd
from sqlalchemy import create_engine
import os

def executar_importacao():
    print("🚀 Iniciando Carga de Dados no Banco ...")
    
    # Configuração da conexão (Coloque sua senha correta)
    engine = create_engine('postgresql://postgres:SUASENHA@localhost:5432/intuitive_db')

    try:
        # 1. Importar Cadastro de Operadoras
        df_cad = pd.read_csv('Relatorio_cadop.csv', sep=';', encoding='latin-1')
        df_cad.columns = [c.strip().upper() for c in df_cad.columns]
        
        operadoras = pd.DataFrame()
        operadoras['registro_ans'] = df_cad['REGISTRO_OPERADORA'].astype(str).str.zfill(6)
        operadoras['cnpj'] = df_cad['CNPJ'].astype(str)
        operadoras['razao_social'] = df_cad['RAZAO_SOCIAL'].fillna('NOME NÃO INFORMADO')
        operadoras['modalidade'] = df_cad['MODALIDADE']
        operadoras['uf'] = df_cad['UF']
        
        operadoras.to_sql('operadoras', engine, if_exists='append', index=False)
        print("   ✅ Tabela 'operadoras' populada.")

        # 2. Importar Despesas Consolidadas
        df_desp = pd.read_csv(os.path.join('saida', 'consolidado_despesas.csv'), sep=';')
        
        despesas = pd.DataFrame()
        despesas['registro_ans'] = df_desp['CNPJ'].astype(str).str.zfill(6)
        despesas['trimestre'] = pd.to_numeric(df_desp['Trimestre'], errors='coerce').fillna(0).astype(int)
        despesas['ano'] = pd.to_numeric(df_desp['Ano'], errors='coerce').fillna(0).astype(int)
        despesas['valor_despesa'] = pd.to_numeric(
            df_desp['ValorDespesas'].astype(str).str.replace(',', '.'), 
            errors='coerce'
        ).fillna(0)

        despesas.to_sql('despesas_consolidadas', engine, if_exists='append', index=False)
        print("   ✅ Tabela 'despesas_consolidadas' populada.")

        # 3. Importar Dados Agregados (NOMES CORRIGIDOS)
        caminho_agregados = os.path.join('saida', 'despesas_agregadas.csv')
        if os.path.exists(caminho_agregados):
            # Lendo o CSV com o separador correto ';'
            df_agreg = pd.read_csv(caminho_agregados, sep=';')
            
            agregados = pd.DataFrame()
            
            # Mapeamento exato conforme as colunas que você enviou:
            agregados['razao_social'] = df_agreg['RazaoSocial'].fillna('NOME NÃO INFORMADO')
            agregados['uf'] = df_agreg['UF'].fillna('ND')
            
            # Tratamento numérico para evitar erros no banco de dados
            agregados['total_despesas'] = pd.to_numeric(
                df_agreg['TotalDespesas'].astype(str).str.replace(',', '.'), 
                errors='coerce'
            ).fillna(0)
            
            agregados['media_trimestral'] = pd.to_numeric(
                df_agreg['MediaTrimestral'].astype(str).str.replace(',', '.'), 
                errors='coerce'
            ).fillna(0)
            
            agregados['desvio_padrao'] = pd.to_numeric(
                df_agreg['DesvioPadraoDespesas'].astype(str).str.replace(',', '.'), 
                errors='coerce'
            ).fillna(0)

            # Inserção no banco de dados
            agregados.to_sql('despesas_agregadas', engine, if_exists='append', index=False)
            print("   ✅ Tabela 'despesas_agregadas' populada com sucesso!")
        else:
            print("   ⚠️ Arquivo 'despesas_agregadas.csv' não encontrado na pasta 'saida'.")

    except Exception as e:
        print(f"❌ Erro durante a importação: {e}")

if __name__ == "__main__":
    executar_importacao()