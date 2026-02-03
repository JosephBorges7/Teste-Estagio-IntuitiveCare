-- Query 1: Top 5 operadoras com maior crescimento percentual entre o 1º e o último trimestre 
-- Justificativa: Uso de CTE para calcular a variação entre períodos extremos.
WITH limites AS (
    SELECT registro_ans, 
           MIN(trimestre) as t_inicial, 
           MAX(trimestre) as t_final
    FROM despesas_consolidadas
    WHERE ano = 2025
    GROUP BY registro_ans
    HAVING COUNT(DISTINCT trimestre) >= 2
),
valores AS (
    SELECT d.registro_ans,
           MAX(CASE WHEN d.trimestre = l.t_inicial THEN d.valor_despesa END) as v_ini,
           MAX(CASE WHEN d.trimestre = l.t_final THEN d.valor_despesa END) as v_fim
    FROM despesas_consolidadas d
    JOIN limites l ON d.registro_ans = l.registro_ans
    WHERE d.ano = 2025
    GROUP BY d.registro_ans
)
SELECT o.razao_social,
    -- Coalesce transforma o resultado final em 0 se for nulo
    COALESCE(
        ((v_fim - v_ini) / NULLIF(v_ini, 0)) * 100, 
        0
    ) as crescimento_percentual
FROM valores v
JOIN operadoras o ON v.registro_ans = o.registro_ans
WHERE v_ini IS NOT NULL AND v_fim IS NOT NULL 
ORDER BY crescimento_percentual DESC
LIMIT 5;

-- Query 2: Distribuição de despesas por UF (Top 5 estados e média) 
SELECT o.uf, 
       TO_CHAR(SUM(d.valor_despesa), 'R$ 9G999G999G999D99') as total_formatado,
       TO_CHAR(AVG(d.valor_despesa), 'R$ 9G999G999G999D99') as media_formatada
FROM despesas_consolidadas d
JOIN operadoras o ON d.registro_ans = o.registro_ans
GROUP BY o.uf
ORDER BY SUM(d.valor_despesa) DESC
LIMIT 5;
-- Query 3: Operadoras com despesas acima da média geral em pelo menos 2 trimestres 
-- Justificativa: Uso de subquery para calcular a média global e filtrar grupos. 
SELECT o.razao_social
FROM despesas_consolidadas d
JOIN operadoras o ON d.registro_ans = o.registro_ans
WHERE d.valor_despesa > (SELECT AVG(valor_despesa) FROM despesas_consolidadas)
GROUP BY o.razao_social
HAVING COUNT(DISTINCT trimestre) >= 2;