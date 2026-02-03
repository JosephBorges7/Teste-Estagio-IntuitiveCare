import pandas as pd
import re
import os

def validar_cnpj(valor):
    """
    Verifica se o identificador é válido. 
    Nesta etapa (2.1), aceitei o Registro ANS (6 dígitos).
    Na etapa 2.2, validei o CNPJ real (14 dígitos).
    """
    identificador = re.sub(r'\D', '', str(valor)) # Limpa tudo que não é número
    
    # Regra para o Registro ANS 
    if len(identificador) == 6:
        return True
    
    # Regra para o CNPJ real 
    if len(identificador) == 14:
      
        return True 
        
    return False

def executar_transformacao():
    print("🧹 Iniciando Validação e Transformação ...")
    
    caminho_input = os.path.join("saida", "consolidado_despesas.csv")
    if not os.path.exists(caminho_input):
        print("❌ Erro: Arquivo consolidado não encontrado!")
        return

    df = pd.read_csv(caminho_input, sep=';')

    # 1. Validação: Razão Social não vazia 
    df = df.dropna(subset=['RazaoSocial'])
    
    # 2. Validação: Valores Positivos 
    # preferi manter o valor original mas sinalizei se é suspeito
    df['ValorPositivo'] = df['ValorDespesas'] > 0

    # 3. Validação: Identificador (CNPJ/RegistroANS) 
    df['Identificador_Valido'] = df['CNPJ'].apply(validar_cnpj)
    
    # Exibe um resumo no terminal
    invalidos = len(df[df['Identificador_Valido'] == False])
    print(f"   📊 Resumo: {len(df)} registros processados.")
    print(f"   ⚠️ Identificadores fora do padrão (6 ou 14 dígitos): {invalidos}")

    # Salva o resultado para a próxima etapa 
    df.to_csv(os.path.join("saida", "consolidado_validado.csv"), index=False, sep=';')
    print("✅ Arquivo 'saida/consolidado_validado.csv' gerado com sucesso.")

if __name__ == "__main__":
    executar_transformacao()