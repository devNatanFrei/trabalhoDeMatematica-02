from ortools.linear_solver import pywraplp

def sem_limites_de_transacao():
    # Criar o solver
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Definir variáveis de decisão
    iene_para_dolar = solver.IntVar(0.0, solver.infinity(), 'iene_para_dolar')
    rupia_para_dolar = solver.IntVar(0.0, solver.infinity(), 'rupia_para_dolar')
    ringgit_para_dolar = solver.IntVar(0.0, solver.infinity(), 'ringgit_para_dolar')

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
        print("Solução ótima encontrada sem limites de transação:")
        print(f"Ienes convertidos em dólares: {iene_para_dolar.solution_value()} dólares")
        print(f"Rúpias convertidas em dólares: {rupia_para_dolar.solution_value()} dólares")
        print(f"Ringgits convertidos em dólares: {ringgit_para_dolar.solution_value()} dólares")
        total_dolares = iene_para_dolar.solution_value() * 0.008 + rupia_para_dolar.solution_value() * 0.00016 + ringgit_para_dolar.solution_value() * 0.25
        print(f"Total em dólares sem limites de transação: {total_dolares}")
    else:
        print("Não foi possível encontrar uma solução ótima.")

# Chamar a função para a parte (c)
sem_limites_de_transacao()
