from ortools.linear_solver import pywraplp

def optimize_transactions():
    # Dados ajustados: custos de troca e limites de transações
    exchange_costs = [
        [0.0000, 0.0050, 0.0050, 0.0040, 0.0040, 0.0040, 0.0025, 0.0050],  # Iene
        [0.0050, 0.0000, 0.0070, 0.0050, 0.0030, 0.0030, 0.0075, 0.0075],  # Rúpia
        [0.0050, 0.0070, 0.0000, 0.0070, 0.0070, 0.0040, 0.0045, 0.0050],  # Ringgit
        [0.0040, 0.0050, 0.0070, 0.0000, 0.0005, 0.0010, 0.0010, 0.0010],  # Dólar Norte-Americano
        [0.0040, 0.0030, 0.0070, 0.0005, 0.0000, 0.0020, 0.0010, 0.0010],  # Dólar Canadense
        [0.0040, 0.0030, 0.0040, 0.0010, 0.0020, 0.0000, 0.0005, 0.0050],  # Euro
        [0.0025, 0.0075, 0.0045, 0.0010, 0.0010, 0.0005, 0.0000, 0.0050],  # Libra
        [0.0050, 0.0075, 0.0050, 0.0010, 0.0010, 0.0050, 0.0050, 0.0000],  # Peso
    ]

    # Limites de transação entre as moedas
    transaction_limits = [
        [0, 5, 5, 2, 2, 2, 2, 4],  # Iene
        [5, 0, 2, 0.2, 0.2, 1, 0.5, 0.2],  # Rúpia
        [3, 4.5, 0, 1.5, 1.5, 2.5, 1, 1],  # Ringgit
    ]

    # Inicializando o solver para programação linear
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        return None

    num_currencies = len(exchange_costs)

    # Criando as variáveis de decisão para transações entre moedas
    transactions = [
        [solver.NumVar(0, solver.infinity(), f"trans_{i}_{j}") for j in range(num_currencies)]
        for i in range(num_currencies)
    ]

    # Definindo o objetivo: minimizar o custo total de transação
    total_cost = solver.Sum(
        exchange_costs[i][j] * transactions[i][j] for i in range(num_currencies) for j in range(num_currencies)
    )
    solver.Minimize(total_cost)

    # Adicionando as restrições de capacidade máxima para cada transação
    for i in range(len(transaction_limits)):
        for j in range(num_currencies):
            solver.Add(transactions[i][j] <= transaction_limits[i][j])

    # Adicionando restrições de saldo inicial para as moedas de origem
    solver.Add(transactions[0][3] + transactions[0][4] + transactions[0][5] + transactions[0][6] + transactions[0][7] == 9.6)  # Iene
    solver.Add(transactions[1][3] + transactions[1][4] + transactions[1][5] + transactions[1][6] + transactions[1][7] == 1.68)  # Rúpia
    solver.Add(transactions[2][3] + transactions[2][4] + transactions[2][5] + transactions[2][6] + transactions[2][7] == 5.6)  # Ringgit

    # Adicionando restrições para manter o balanço em moedas intermediárias
    for idx in range(4, 8):
        solver.Add(
            solver.Sum(transactions[idx][j] for j in range(num_currencies)) ==
            solver.Sum(transactions[i][idx] for i in range(num_currencies))
        )

    # Resolvendo o problema
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print("Solução ótima encontrada:")
        print(f"Custo total de transação: {solver.Objective().Value():.4f} milhões")

        currency_names = ["Iene", "Rúpia", "Ringgit", "Dólar Norte-Americano", "Dólar Canadense", "Euro", "Libra", "Peso"]
        for i in range(num_currencies):
            for j in range(num_currencies):
                amount = transactions[i][j].solution_value()
                if amount > 0:
                    print(f"{currency_names[i]} -> {currency_names[j]}: {amount:.2f}")
    else:
        print("Nenhuma solução viável ou erro durante a otimização.")


# Executando a função
optimize_transactions()
