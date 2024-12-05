from ortools.linear_solver import pywraplp

# Tabelas de custo e capacidade ajustadas
taxas_cambio = [
    # |Iene|Rúpia|Ringgit|Dólar Americano|Dólar Canadense|Euro|Libra|Peso|
    [0.0000, 0.0050, 0.0050, 0.0040, 0.0040, 0.0040, 0.0025, 0.0050],  # Iene 0
    [0.0050, 0.0000, 0.0070, 0.0050, 0.0030, 0.0030, 0.0075, 0.0075],  # Rúpia 1
    [0.0050, 0.0070, 0.0000, 0.0070, 0.0070, 0.0040, 0.0045, 0.0050],  # Ringgit 2
    [0.0040, 0.0050, 0.0070, 0.0000, 0.0005, 0.0010, 0.0010, 0.0010],  # Dólar Americano 3
    [0.0040, 0.0030, 0.0070, 0.0005, 0.0000, 0.0020, 0.0010, 0.0010],  # Dólar Canadense 4
    [0.0040, 0.0030, 0.0040, 0.0010, 0.0020, 0.0000, 0.0005, 0.0050],  # Euro 5
    [0.0025, 0.0075, 0.0045, 0.0010, 0.0010, 0.0005, 0.0000, 0.0050],  # Libra 6
    [0.0050, 0.0075, 0.0050, 0.0010, 0.0010, 0.0050, 0.0050, 0.0000],  # Peso 7
]

limites_transacao = [
    # |Iene|Rúpia|Ringgit|Dólar Americano|Dólar Canadense|Euro|Libra|Peso|
    [0, 5, 5, 2, 2, 2, 2, 4],  # Iene
    [5, 0, 2, 0.2, 0.2, 1, 0.5, 0.2],  # Rúpia
    [3, 4.5, 0, 1.5, 1.5, 2.5, 1, 1]  # Ringgit
]

def calculo():
    # Criação do solver utilizando o "GLOP" para problemas de otimização reais
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        return None
    
    n = len(taxas_cambio)  # Quantidade de moedas (tamanho das tabelas)
    
    # Definição das variáveis de transação x[i][j] (de i para j)
    # x[i][j] representa a quantidade de moeda i sendo trocada por moeda j
    x = []
    for i in range(n):
        x.append([])
        for j in range(n):
            # Criação de uma variável de decisão, onde a transação x[i][j] é >= 0
            x[i].append(solver.NumVar(0, solver.infinity(), f"x{i}{j}"))
    
    # Função objetivo: Minimizar o custo total das transações
    objetivo = solver.Sum(taxas_cambio[i][j] * x[i][j] for i in range(n) for j in range(n))
    solver.Minimize(objetivo)
    
    # Condições: Capacidade das transações (limites de cada moeda para outra)
    for i in range(3):  # Limite de capacidade é definido para as 3 primeiras moedas (Iene, Rúpia, Ringgit)
        for j in range(n):
            # Adiciona a restrição de que as transações de moeda i para moeda j não ultrapassem o limite de capacidade
            solver.Add(x[i][j] <= limites_transacao[i][j])
    
    # Fontes (moedas de origem) - as transações totais das fontes devem somar um valor específico
    solver.Add(x[0][3] + x[0][4] + x[0][5] + x[0][6] + x[0][7] - 9.6 == 0)  # Iene
    solver.Add(x[1][3] + x[1][4] + x[1][5] + x[1][6] + x[1][7] - 1.68 == 0)  # Rúpia
    solver.Add(x[2][3] + x[2][4] + x[2][5] + x[2][6] + x[2][7] - 5.6 == 0)  # Ringgit
    
    # Sumidouro (as transações que saem das moedas intermediárias)
    solver.Add(16.88 - x[0][3] - x[1][3] - x[2][3] - x[4][3] - x[5][3] - x[6][3] - x[7][3] == 0)
    
    # Intermediário (relaciona transações entre diferentes moedas intermediárias)
    solver.Add(x[4][3] + x[4][5] + x[4][6] + x[4][7] - x[0][4] - x[1][4] - x[2][4] - x[5][4] - x[6][4] - x[7][4] == 0)
    solver.Add(x[5][3] + x[5][4] + x[5][6] + x[5][7] - x[0][5] - x[1][5] - x[2][5] - x[4][5] - x[6][5] - x[7][5] == 0)
    solver.Add(x[6][3] + x[6][4] + x[6][5] + x[6][7] - x[0][6] - x[1][6] - x[2][6] - x[4][6] - x[5][6] - x[7][6] == 0)
    solver.Add(x[7][3] + x[7][4] + x[7][5] + x[7][6] - x[0][7] - x[1][7] - x[2][7] - x[4][7] - x[5][7] - x[6][7] == 0)

    # Resolvemos o problema de otimização
    viavel = solver.Solve()
    if viavel == pywraplp.Solver.OPTIMAL:
        print("Solução encontrada:")
        print(f"Função Objetivo = {solver.Objective().Value():0.4f} milhões de U$")
        
        # Exibição dos resultados das transações
        moedas = ["Iene", "Rúpia", "Ringgit", "Dólar Americano", "Dólar Canadense", "Euro", "Libra", "Peso"]
        
        for i in range(n):
            print(f"Transações de {moedas[i]} (em Milhões de U$):")
            for j in range(n):
                valor_transacao = x[i][j].solution_value()
                if valor_transacao > 0:  # Exibe apenas transações com valor positivo
                    print(f"{moedas[i]} para {moedas[j]}: {valor_transacao:.2f}")
            print("-" * 50)
    else:
        print("Solução inviável")

# Chamada da função
calculo()
