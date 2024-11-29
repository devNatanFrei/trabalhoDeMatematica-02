from ortools.linear_solver import pywraplp

def transacoes_ideais():
    # Criar o solver
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Definir variáveis de decisão: quanto de cada moeda vai ser convertida para dólares
    iene_para_dolar = solver.IntVar(0.0, 15000000, 'iene_para_dolar')  # O limite máximo de ienes é 15.000.000
    rupia_para_dolar = solver.IntVar(0.0, 105000000, 'rupia_para_dolar')  # Limite de rúpias disponível
    ringgit_para_dolar = solver.IntVar(0.0, 28000000, 'ringgit_para_dolar')  # Limite de ringgits disponível

    # Função objetivo: Maximizar o valor total em dólares
    # Taxas de conversão de acordo com as tabelas fornecidas
    solver.Maximize(
        0.008 * iene_para_dolar + 0.00016 * rupia_para_dolar + 0.25 * ringgit_para_dolar
    )

    # Restrições de quantidade de cada moeda disponível
    solver.Add(iene_para_dolar <= 15000000)  # Limite de ienes (15 milhões)
    solver.Add(rupia_para_dolar <= 105000000)  # Limite de rúpias (10,5 bilhões)
    solver.Add(ringgit_para_dolar <= 28000000)  # Limite de ringgits (28 milhões)

    # Resolver o problema
    status = solver.Solve()

    # Verificar o status da solução
    if status == pywraplp.Solver.OPTIMAL:
        print("Transações ideais para converter as posições em dólares:")
        print(f"Ienes convertidos em dólares: {iene_para_dolar.solution_value()} dólares")
        print(f"Rúpias convertidas em dólares: {rupia_para_dolar.solution_value()} dólares")
        print(f"Ringgits convertidos em dólares: {ringgit_para_dolar.solution_value()} dólares")
        
        # Calcular o total em dólares após as transações
        total_dolares = (
            0.008 * iene_para_dolar.solution_value() + 
            0.00016 * rupia_para_dolar.solution_value() + 
            0.25 * ringgit_para_dolar.solution_value()
        )
        print(f"Total em dólares após as transações: {total_dolares}")
    else:
        print("Não foi possível encontrar uma solução ótima.")

# Chamar a função para a parte (b)
transacoes_ideais()
