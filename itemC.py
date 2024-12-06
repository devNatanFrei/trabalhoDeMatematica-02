from ortools.linear_solver import pywraplp

def optimize_transactions():
    # Custos de transação (matriz de custos)
    exchange_costs = [
        [0.0000, 0.0050, 0.0050, 0.0040, 0.0040, 0.0040, 0.0025, 0.0050],  # Yen
        [0.0050, 0.0000, 0.0070, 0.0050, 0.0030, 0.0030, 0.0075, 0.0075],  # Rupee
        [0.0050, 0.0070, 0.0000, 0.0070, 0.0070, 0.0040, 0.0045, 0.0050],  # Ringgit
        [0.0040, 0.0050, 0.0070, 0.0000, 0.0005, 0.0010, 0.0010, 0.0010],  # US Dollar
        [0.0040, 0.0030, 0.0070, 0.0005, 0.0000, 0.0020, 0.0010, 0.0010],  # Canadian Dollar
        [0.0040, 0.0030, 0.0040, 0.0010, 0.0020, 0.0000, 0.0005, 0.0050],  # Euro
        [0.0025, 0.0075, 0.0045, 0.0010, 0.0010, 0.0005, 0.0000, 0.0050],  # Pound
        [0.0050, 0.0075, 0.0050, 0.0010, 0.0010, 0.0050, 0.0050, 0.0000],  # Peso
    ]

    # Inicializando o solver
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        return None

    num_currencies = len(exchange_costs)

    # Criando variáveis de decisão para as transações
    transactions = []
    for i in range(num_currencies):
        row = []
        for j in range(num_currencies):
            row.append(solver.NumVar(0, solver.infinity(), f"trans_{i}_{j}"))
        transactions.append(row)

    # Função objetivo: minimizar o custo total da transação
    total_cost = solver.Sum(
        exchange_costs[i][j] * transactions[i][j]
        for i in range(num_currencies)
        for j in range(num_currencies)
    )
    solver.Minimize(total_cost)

    # Adicionando as restrições de transações de fontes
    solver.Add(transactions[0][3] + transactions[0][4] + transactions[0][5] + transactions[0][6] + transactions[0][7] == 9.6)  # Yen
    solver.Add(transactions[1][3] + transactions[1][4] + transactions[1][5] + transactions[1][6] + transactions[1][7] == 1.68)  # Rupee
    solver.Add(transactions[2][3] + transactions[2][4] + transactions[2][5] + transactions[2][6] + transactions[2][7] == 5.6)  # Ringgit

    # Adicionando as restrições de equilíbrio de transações
    for i in range(4, 8):  # De Dólar Canadense a Peso
        outgoing = solver.Sum(transactions[i][j] for j in range(num_currencies))
        incoming = solver.Sum(transactions[x][i] for x in range(num_currencies))
        solver.Add(outgoing == incoming)

    # Resolvendo o problema de otimização
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found:")
        print(f"Total transaction cost: {solver.Objective().Value():.4f} million USD")

        currency_names = [
            "Yen", "Rupee", "Ringgit", "US Dollar",
            "Canadian Dollar", "Euro", "Pound", "Peso"
        ]
        for i in range(num_currencies):
            for j in range(num_currencies):
                amount = transactions[i][j].solution_value()
                if amount > 0:
                    print(f"{currency_names[i]} -> {currency_names[j]}: {amount:.2f}")
    else:
        print("No feasible solution or error during optimization.")

# Executando a função
optimize_transactions()
