from ortools.linear_solver import pywraplp

# Custos de conversão entre as moedas
taxas_cambio = [
    [0.0000, 0.0050, 0.0050, 0.0040, 0.0040, 0.0040, 0.0025, 0.0050],  # Iene
    [0.0050, 0.0000, 0.0070, 0.0050, 0.0030, 0.0030, 0.0075, 0.0075],  # Rúpia
    [0.0050, 0.0070, 0.0000, 0.0070, 0.0070, 0.0040, 0.0045, 0.0050],  # Ringgit
    [0.0040, 0.0050, 0.0070, 0.0000, 0.0005, 0.0010, 0.0010, 0.0010],  # Dólar Norte Americano
    [0.0040, 0.0030, 0.0070, 0.0005, 0.0000, 0.0020, 0.0010, 0.0010],  # Dólar Canadense
    [0.0040, 0.0030, 0.0040, 0.0010, 0.0020, 0.0000, 0.0005, 0.0050],  # Euro
    [0.0025, 0.0075, 0.0045, 0.0010, 0.0010, 0.0005, 0.0000, 0.0050],  # Libra
    [0.0050, 0.0075, 0.0050, 0.0010, 0.0010, 0.0050, 0.0050, 0.0000]   # Peso
]

# Função para aplicar a taxa de aumento ao custo da moeda
def aplicar_taxa(indice, taxa):
    for i in range(len(taxas_cambio)):
        taxas_cambio[indice][i] *= taxa / 100

def Calcular():
    # Criação do solver utilizando o "GLOP" para problemas de otimização reais
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        return None
    
    n = len(taxas_cambio)
    
    # Definição de variáveis
    x = []
    for i in range(n):
        linha = []
        for j in range(n):
            variavel = solver.NumVar(0, solver.infinity(), f"x{i}{j}")
            linha.append(variavel)
        x.append(linha)
    
    # Aumentando o custo da Rúpia em 500%
    aplicar_taxa(1, 500)
    
    # Função objetivo de minimização
    objetivo = solver.Sum(
        taxas_cambio[i][j] * x[i][j] for i in range(n) for j in range(n)
    )
    solver.Minimize(objetivo)
    
    # Condições:
    # Fontes
    solver.Add(x[0][3] + x[0][4] + x[0][5] + x[0][6] + x[0][7] - 9.6 == 0)  # Iene
    solver.Add(x[1][3] + x[1][4] + x[1][5] + x[1][6] + x[1][7] - 1.68 == 0)  # Rúpia
    solver.Add(x[2][3] + x[2][4] + x[2][5] + x[2][6] + x[2][7] - 5.6 == 0)  # Ringgit
    
    # Sumidouro
    solver.Add(16.88 - x[0][3] - x[1][3] - x[2][3] - x[4][3] - x[5][3] - x[6][3] - x[7][3] == 0)
    
    # Intermediário
    solver.Add(x[4][3] + x[4][5] + x[4][6] + x[4][7] - x[0][4] - x[1][4] - x[2][4] - x[5][4] - x[6][4] - x[7][4] == 0)
    solver.Add(x[5][3] + x[5][4] + x[5][6] + x[5][7] - x[0][5] - x[1][5] - x[2][5] - x[4][5] - x[6][5] - x[7][5] == 0)
    solver.Add(x[6][3] + x[6][4] + x[6][5] + x[6][7] - x[0][6] - x[1][6] - x[2][6] - x[4][6] - x[5][6] - x[7][6] == 0)
    solver.Add(x[7][3] + x[7][4] + x[7][5] + x[7][6] - x[0][7] - x[1][7] - x[2][7] - x[4][7] - x[5][7] - x[6][7] == 0)
    
    # Resolvendo o problema
    viavel = solver.Solve()
    
    if viavel == pywraplp.Solver.OPTIMAL:
        print("Solução encontrada:")
        print(f"Função Objetivo = {solver.Objective().Value():0.4f} milhões de U$")
        
        # Exibindo as transações de cada moeda
        moedas = ["Iene", "Rúpia", "Ringgit", "Dólar Norte Americano", "Dólar Canadense", "Euro", "Libra", "Peso"]
        
        for i in range(3):  # Para as 3 primeiras moedas (Iene, Rúpia, Ringgit)
            print(f"\nTransações de {moedas[i]} (em Milhões de U$):")
            for j in range(n):
                valor_transacao = x[i][j].solution_value()
                if valor_transacao > 0:  # Exibe transações com valor positivo
                    print(f"{moedas[i]} para {moedas[j]}: {valor_transacao:.2f}")
            print("-" * 50)
        
        # Exibindo transações intermediárias
        print("\nTransações Intermediárias (em Milhões de U$):")
        print(f"Dólar Canadense para Dólar Norte Americano: {(x[4][3].solution_value()):.2f}")
        print(f"Euro para Dólar Norte Americano: {(x[5][3].solution_value()):.2f}")
        print(f"Libra para Dólar Norte Americano: {(x[6][3].solution_value()):.2f}")
        print(f"Peso para Dólar Norte Americano: {(x[7][3].solution_value()):.2f}")
    
    else:
        print("Solução inviável")

# Chamada da função Calcular
Calcular()
