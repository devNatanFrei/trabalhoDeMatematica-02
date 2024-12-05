from ortools.linear_solver import pywraplp

def Calculo():
    # Custos de conversão entre as moedas
    Iene = [0.0000, 0.0050, 0.0050, 0.0040, 0.0040, 0.0040, 0.0025, 0.0050]
    Rupia = [0.0050, 0.0000, 0.0070, 0.0050, 0.0030, 0.0030, 0.0075, 0.0075]
    Ringgit = [0.0050, 0.0070, 0.0000, 0.0070, 0.0070, 0.0040, 0.0045, 0.0050]
    Dolar_Norte_Americano = [0.0040, 0.0050, 0.0070, 0.0000, 0.0005, 0.0010, 0.0010, 0.0010]
    Dolar_Canadense = [0.0040, 0.0030, 0.0070, 0.0005, 0.0000, 0.0020, 0.0010, 0.0010]
    Euro = [0.0040, 0.0030, 0.0040, 0.0010, 0.0020, 0.0000, 0.0005, 0.0050]
    Libra = [0.0025, 0.0075, 0.0045, 0.0010, 0.0010, 0.0005, 0.0000, 0.0050]
    Peso = [0.0050, 0.0075, 0.0050, 0.0010, 0.0010, 0.0050, 0.0050, 0.0000]

    # Criação do solver utilizando o "GLOP" para problemas de otimização reais
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        return None
    
    moedas = [Iene, Rupia, Ringgit, Dolar_Norte_Americano, Dolar_Canadense, Euro, Libra, Peso]
    num_moedas = len(moedas)  # Número de moedas
    
    # Definição das variáveis de decisão
    transacoes = []
    for i in range(num_moedas):
        transacoes.append([])
        for j in range(num_moedas):
            transacoes[i].append(solver.NumVar(0, solver.infinity(), f"x{i}{j}"))
    
    # Função objetivo de minimização
    solver.Minimize(solver.Sum(moedas[i][j] * transacoes[i][j] for i in range(num_moedas) for j in range(num_moedas)))
    
    # Condições:
    # Fontes (moedas de origem)
    solver.Add(transacoes[0][3] + transacoes[0][4] + transacoes[0][5] + transacoes[0][6] + transacoes[0][7] - 9.6 == 0)  # Iene
    solver.Add(transacoes[1][3] + transacoes[1][4] + transacoes[1][5] + transacoes[1][6] + transacoes[1][7] - 1.68 == 0)  # Rúpia
    solver.Add(transacoes[2][3] + transacoes[2][4] + transacoes[2][5] + transacoes[2][6] + transacoes[2][7] - 5.6 == 0)  # Ringgit
    
    # Sumidouro (destino das transações)
    solver.Add(16.88 - transacoes[0][3] - transacoes[1][3] - transacoes[2][3] - transacoes[4][3] - transacoes[5][3] - transacoes[6][3] - transacoes[7][3] == 0)
    
    # Intermediário (relações entre transações)
    solver.Add(transacoes[4][3] + transacoes[4][5] + transacoes[4][6] + transacoes[4][7] - transacoes[0][4] - transacoes[1][4] - transacoes[2][4] - transacoes[5][4] - transacoes[6][4] - transacoes[7][4] == 0)
    solver.Add(transacoes[5][3] + transacoes[5][4] + transacoes[5][6] + transacoes[5][7] - transacoes[0][5] - transacoes[1][5] - transacoes[2][5] - transacoes[4][5] - transacoes[6][5] - transacoes[7][5] == 0)
    solver.Add(transacoes[6][3] + transacoes[6][4] + transacoes[6][5] + transacoes[6][7] - transacoes[0][6] - transacoes[1][6] - transacoes[2][6] - transacoes[4][6] - transacoes[5][6] - transacoes[7][6] == 0)
    solver.Add(transacoes[7][3] + transacoes[7][4] + transacoes[7][5] + transacoes[7][6] - transacoes[0][7] - transacoes[1][7] - transacoes[2][7] - transacoes[4][7] - transacoes[5][7] - transacoes[6][7] == 0)
    
    # Resolvendo o problema
    viavel = solver.Solve()
    
    if viavel == pywraplp.Solver.OPTIMAL:
        print("Solução encontrada:")
        print(f"Função Objetivo = {solver.Objective().Value():0.4f} milhões de U$")
        
        # Exibindo as transações
        nomes_moedas = ["Iene", "Rúpia", "Ringgit", "Dólar Norte Americano", "Dólar Canadense", "Euro", "Libra", "Peso"]
        
        for i in range(3):  # Para as 3 primeiras moedas (Iene, Rúpia, Ringgit)
            print(f"\nTransações de {nomes_moedas[i]} (em Milhões de U$):")
            for j in range(num_moedas):
                valor_transacao = transacoes[i][j].solution_value()
                if valor_transacao > 0:  # Exibe transações com valor positivo
                    print(f"{nomes_moedas[i]} para {nomes_moedas[j]}: {valor_transacao:.2f}")
            print("-" * 50)
        
        print("\nTransações Intermediárias (em Milhões de U$):")
        print(f"Dólar Canadense para Dólar Norte Americano: {(transacoes[4][3].solution_value()):.2f}")
        print(f"Euro para Dólar Norte Americano: {(transacoes[5][3].solution_value()):.2f}")
        print(f"Libra para Dólar Norte Americano: {(transacoes[6][3].solution_value()):.2f}")
        print(f"Peso para Dólar Norte Americano: {(transacoes[7][3].solution_value()):.2f}")
    
    else:
        print("Solução inviável")

# Chamada da função Fluxo
Calculo()
