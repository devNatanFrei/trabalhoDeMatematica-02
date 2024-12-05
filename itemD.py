from ortools.linear_solver import pywraplp

def Calculate():
    # Cria o solver usando "GLOP" para problemas reais de otimização
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        return None
    
    # Custos de conversão entre moedas
    exchange_rates = [
        [0.0000, 0.0050, 0.0050, 0.0040, 0.0040, 0.0040, 0.0025, 0.0050],  # Yen
        [0.0050, 0.0000, 0.0070, 0.0050, 0.0030, 0.0030, 0.0075, 0.0075],  # Rupee
        [0.0050, 0.0070, 0.0000, 0.0070, 0.0070, 0.0040, 0.0045, 0.0050],  # Ringgit
        [0.0040, 0.0050, 0.0070, 0.0000, 0.0005, 0.0010, 0.0010, 0.0010],  # US Dollar
        [0.0040, 0.0030, 0.0070, 0.0005, 0.0000, 0.0020, 0.0010, 0.0010],  # Canadian Dollar
        [0.0040, 0.0030, 0.0040, 0.0010, 0.0020, 0.0000, 0.0005, 0.0050],  # Euro
        [0.0025, 0.0075, 0.0045, 0.0010, 0.0010, 0.0005, 0.0000, 0.0050],  # Pound
        [0.0050, 0.0075, 0.0050, 0.0010, 0.0010, 0.0050, 0.0050, 0.0000]   # Peso
    ]

    n = len(exchange_rates)

    # Definindo variáveis
    transactions = []
    for i in range(n):
        row = []
        for j in range(n):
            variable = solver.NumVar(0, solver.infinity(), f"x{i}{j}")
            row.append(variable)
        transactions.append(row)

    # Aumenta o custo da Rúpia em 500%
    for i in range(n):
        exchange_rates[1][i] *= 5  # 500% aumento

    # Função objetivo para minimização
    objective = solver.Sum(
        exchange_rates[i][j] * transactions[i][j] for i in range(n) for j in range(n)
    )
    solver.Minimize(objective)
    
    # Restrições:
    # Fontes (moedas de origem)
    solver.Add(transactions[0][3] + transactions[0][4] + transactions[0][5] + transactions[0][6] + transactions[0][7] - 9.6 == 0)  # Yen
    solver.Add(transactions[1][3] + transactions[1][4] + transactions[1][5] + transactions[1][6] + transactions[1][7] - 1.68 == 0)  # Rupee
    solver.Add(transactions[2][3] + transactions[2][4] + transactions[2][5] + transactions[2][6] + transactions[2][7] - 5.6 == 0)  # Ringgit
    
    # Sink (moeda final em US Dollars)
    solver.Add(16.88 - transactions[0][3] - transactions[1][3] - transactions[2][3] - transactions[4][3] - transactions[5][3] - transactions[6][3] - transactions[7][3] == 0)
    
    # Moedas intermediárias
    solver.Add(transactions[4][3] + transactions[4][5] + transactions[4][6] + transactions[4][7] - transactions[0][4] - transactions[1][4] - transactions[2][4] - transactions[5][4] - transactions[6][4] - transactions[7][4] == 0)
    solver.Add(transactions[5][3] + transactions[5][4] + transactions[5][6] + transactions[5][7] - transactions[0][5] - transactions[1][5] - transactions[2][5] - transactions[4][5] - transactions[6][5] - transactions[7][5] == 0)
    solver.Add(transactions[6][3] + transactions[6][4] + transactions[6][5] + transactions[6][7] - transactions[0][6] - transactions[1][6] - transactions[2][6] - transactions[4][6] - transactions[5][6] - transactions[7][6] == 0)
    solver.Add(transactions[7][3] + transactions[7][4] + transactions[7][5] + transactions[7][6] - transactions[0][7] - transactions[1][7] - transactions[2][7] - transactions[4][7] - transactions[5][7] - transactions[6][7] == 0)
    
    # Resolve o problema
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found:")
        print(f"Total transaction cost: {solver.Objective().Value():.4f} million")

        currency_names = ["Yen", "Rupee", "Ringgit", "US Dollar", "Canadian Dollar", "Euro", "Pound", "Peso"]
        for i in range(n):
            for j in range(n):
                amount = transactions[i][j].solution_value()
                if amount > 0:
                    print(f"{currency_names[i]} -> {currency_names[j]}: {amount:.2f} million")
    else:
        print("No feasible solution or error during optimization.")

# Call the Calculate function
Calculate()
