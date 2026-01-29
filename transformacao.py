import pandas as pd
import re
import os

def validar_cnpj(cnpj):
    """Valida o formato e os dígitos verificadores de um CNPJ."""
    cnpj = re.sub(r'\D', '', str(cnpj)) # Remove caracteres não numéricos
    
    if len(cnpj) != 14 or len(set(cnpj)) == 1:
        return False

    def calcular_digito(cnpj, pesos):
        soma = sum(int(a) * b for a, b in zip(cnpj, pesos))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    # Validação do primeiro dígito
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    if int(cnpj[12]) != calcular_digito(cnpj[:12], pesos1):
        return False

    # Validação do segundo dígito
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    if int(cnpj[13]) != calcular_digito(cnpj[:13], pesos2):
        return False

    return True

def executar_transformacao():
    print("🧹 Iniciando Validação e Transformação...")
    
    # Carrega o consolidado da etapa anterior
    caminho_input = os.path.join("saida", "consolidado_despesas.csv")
    if not os.path.exists(caminho_input):
        print("❌ Erro: Arquivo consolidado não encontrado. Execute a Etapa 1 primeiro.")
        return

    df = pd.read_csv(caminho_input, sep=';')

    # Validação de Razão Social não vazia
    df = df.dropna(subset=['RazaoSocial'])
    
    # Validação de Valores Positivos ( o que for negativo para não afetar somas)
    df['ValorDespesas'] = df['ValorDespesas'].apply(lambda x: x if x > 0 else 0)

    # Validação de CNPJ (Aplicando a função matemática)
    # Criado uma coluna de status para auditoria posterior
    df['CNPJ_Valido'] = df['CNPJ'].apply(validar_cnpj)
    
    qtd_invalidos = len(df[df['CNPJ_Valido'] == False])
    print(f"   ⚠️ Encontrados {qtd_invalidos} registros com CNPJ inválido.")

    # Salva o resultado intermediário
    df.to_csv(os.path.join("saida", "consolidado_validado.csv"), index=False, sep=';')
    print("✅ Etapa 2.1 finalizada: 'saida/consolidado_validado.csv' gerado.")

if __name__ == "__main__":
    executar_transformacao()