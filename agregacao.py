import pandas as pd
import os

def executar_agregacao():
    print("📊 Iniciando Agregação e Análise Estatística...")
    
    caminho_input = os.path.join("saida", "consolidado_enriquecido.csv")
    if not os.path.exists(caminho_input):
        print("❌ Erro: Arquivo enriquecido não encontrado!")
        return

    # 1. Carregar os dados
    df = pd.read_csv(caminho_input, sep=';')

    # 2. Agrupamento e Cálculos (Requisito 2.3)
    # Agrupa por RazaoSocial e UF 
    # Calcula: Total, Média por Trimestre e Desvio Padrão 
    agregado = df.groupby(['RazaoSocial', 'UF']).agg(
        TotalDespesas=('ValorDespesas', 'sum'),
        MediaTrimestral=('ValorDespesas', 'mean'),
        DesvioPadraoDespesas=('ValorDespesas', 'std')
    ).reset_index()

    # 3. Tratamento de Inconsistências Estatísticas
    # Operadoras com apenas 1 registro terão Desvio Padrão 'NaN'. Substituí por 0.
    agregado['DesvioPadraoDespesas'] = agregado['DesvioPadraoDespesas'].fillna(0)

    # 4. Ordenação (Requisito 2.3)
    # Ordenar por valor total (maior para menor) 
    # Trade-off técnico: Ordenação em memória via Pandas 
    agregado = agregado.sort_values(by='TotalDespesas', ascending=False)

    # 5. Exportação (Requisito 2.3)
    caminho_saida = os.path.join("saida", "despesas_agregadas.csv")
    agregado.to_csv(caminho_saida, index=False, sep=';', encoding='utf-8-sig')
    
    print(f"✅ Sucesso! Relatório agregado gerado: {caminho_saida}")
    print(f"   📈 Total de operadoras/UF analisadas: {len(agregado)}")

if __name__ == "__main__":
    executar_agregacao()