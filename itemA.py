from ortools.linear_solver import pywraplp

def fluxo_custo_minimo():
    # Criar o solver
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Definir variáveis de decisão (quantidade de moeda a ser trocada entre os pares)
    iene_para_dolar = solver.IntVar(0.0, 20000000, 'iene_para_dolar')
    rupia_para_dolar = solver.IntVar(0.0, 5000000, 'rupia_para_dolar')
    ringgit_para_dolar = solver.IntVar(0.0, 10000000, 'ringgit_para_dolar')

    # Função objetivo: Maximizar o valor total em dólares
    solver.Maximize(
        0.008 * iene_para_dolar + 0.00016 * rupia_para_dolar + 0.25 * ringgit_para_dolar
    )

    # Restrições de quantidade de cada moeda disponível
    solver.Add(iene_para_dolar <= 25000000)
    solver.Add(rupia_para_dolar <= 105000000)
    solver.Add(ringgit_para_dolar <= 28000000)

    # Resolver o problema
    status = solver.Solve()

    # Verificar o status da solução
    if status == pywraplp.Solver.OPTIMAL:
        print("Solução ótima encontrada para o fluxo com limites de transação:")
        print(f"Ienes convertidos em dólares: {iene_para_dolar.solution_value()} dólares")
        print(f"Rúpias convertidas em dólares: {rupia_para_dolar.solution_value()} dólares")
        print(f"Ringgits convertidos em dólares: {ringgit_para_dolar.solution_value()} dólares")
        total_dolares = iene_para_dolar.solution_value() * 0.008 + rupia_para_dolar.solution_value() * 0.00016 + ringgit_para_dolar.solution_value() * 0.25
        print(f"Total em dólares após todas as transações: {total_dolares}")
    else:
        print("Não foi possível encontrar uma solução ótima.")

# Chamar a função para a parte (a)
fluxo_custo_minimo()
