import os
import requests
from bs4 import BeautifulSoup
import zipfile
import pandas as pd
import glob
import re
from urllib.parse import urljoin

# --- CONFIGURAÇÕES ---
BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def configurar_ambiente():
    for pasta in ["dados_brutos", "dados_extraidos", "saida"]:
        os.makedirs(pasta, exist_ok=True)

def buscar_e_baixar_ultimos_3(url_base):
    print("🔍 Buscando arquivos no site da ANS...")
    res = requests.get(url_base, headers=HEADERS)
    soup = BeautifulSoup(res.text, 'html.parser')
    anos = sorted([urljoin(url_base, a.get('href')) for a in soup.find_all('a') 
                  if a.get('href', '').endswith('/') and a.get('href')[:-1].isdigit()], reverse=True)
    
    arquivos_encontrados = []
    for url_ano in anos:
        if len(arquivos_encontrados) >= 3: break
        res_ano = requests.get(url_ano, headers=HEADERS)
        soup_ano = BeautifulSoup(res_ano.text, 'html.parser')
        zips = sorted([ (a.get('href'), urljoin(url_ano, a.get('href'))) for a in soup_ano.find_all('a') 
                       if a.get('href', '').lower().endswith('.zip') and 'T' in a.get('href').upper()], reverse=True)
        for nome, url_zip in zips:
            if len(arquivos_encontrados) < 3: arquivos_encontrados.append((nome, url_zip))

    for nome, url_zip in arquivos_encontrados:
        caminho_zip = os.path.join("dados_brutos", nome)
        if not os.path.exists(caminho_zip):
            print(f"   ⬇️ Baixando: {nome}")
            r = requests.get(url_zip, stream=True)
            with open(caminho_zip, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): f.write(chunk)
        
        pasta_destino = os.path.join("dados_extraidos", nome.replace('.zip', ''))
        if not os.path.exists(pasta_destino):
            with zipfile.ZipFile(caminho_zip, 'r') as zip_ref: zip_ref.extractall(pasta_destino)
            print(f"   📦 Extraído: {nome}")

def processar_e_consolidar():
    print("\n🔍 Analisando conteúdo técnico dos arquivos...")
    dados_finais = []
    
    arquivos = glob.glob("dados_extraidos/**/*.*", recursive=True)
    for caminho in arquivos:
        nome_arq = os.path.basename(caminho).lower()
        if not nome_arq.endswith(('.csv', '.txt')): continue

        try:
          
            df = pd.read_csv(caminho, sep=';', encoding='utf-8-sig', on_bad_lines='skip')
            
            # Filtrar apenas Despesas com Eventos/Sinistros
            filtro_despesas = df[df['DESCRICAO'].str.contains('EVENTOS|SINISTROS', case=False, na=False)]
            
            if not filtro_despesas.empty:
                # Extração de metadados do nome do arquivo 
                match = re.search(r'(\d)T(\d{4})', caminho.upper())
                filtro_despesas['Trimestre'] = match.group(1) if match else "N/A"
                filtro_despesas['Ano'] = match.group(2) if match else "N/A"
                
                # Mapeamento para o Requisito 1.3
                df_temp = pd.DataFrame()
                df_temp['CNPJ'] = filtro_despesas['REG_ANS'] # Mapeamos o ID disponível
                df_temp['RazaoSocial'] = filtro_despesas['DESCRICAO'] 
                df_temp['Trimestre'] = filtro_despesas['Trimestre']
                df_temp['Ano'] = filtro_despesas['Ano']
                df_temp['ValorDespesas'] = filtro_despesas['VL_SALDO_FINAL']
                
                dados_finais.append(df_temp)
                print(f"   ✅ {len(df_temp)} linhas de despesas extraídas de {nome_arq}")

        except Exception as e:
            print(f"   ⚠️ Erro ao processar {nome_arq}: {e}")

    if dados_finais:
        df_final = pd.concat(dados_finais, ignore_index=True)
        
        # Tratamento de Inconsistências 
        # Limpeza de valores (vírgula para ponto)
        df_final['ValorDespesas'] = pd.to_numeric(
            df_final['ValorDespesas'].astype(str).str.replace(',', '.'), 
            errors='coerce'
        ).fillna(0)
        
        # Remover duplicatas por Operadora/Período
        df_final = df_final.drop_duplicates(subset=['CNPJ', 'Trimestre', 'Ano'], keep='last')
        
        # Exportação Final
        caminho_csv = os.path.join("saida", "consolidado_despesas.csv")
        df_final.to_csv(caminho_csv, index=False, sep=';', encoding='utf-8-sig')
        
        with zipfile.ZipFile(os.path.join("saida", "consolidado_despesas.zip"), 'w') as z:
            z.write(caminho_csv, "consolidado_despesas.csv")
        print(f"\n🚀 SUCESSO! O arquivo agora contém as colunas do Requisito 1.3.")
    else:
        print("\n❌ Nenhuma linha de despesa encontrada. Verifique se o termo 'EVENTOS' ou 'SINISTROS' existe na coluna DESCRICAO.")

if __name__ == "__main__":
    
    configurar_ambiente()
    
   
    buscar_e_baixar_ultimos_3(BASE_URL)
    
   
    processar_e_consolidar()