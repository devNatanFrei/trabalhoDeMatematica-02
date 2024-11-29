from ortools.linear_solver import pywraplp

def com_imposto_de_500():
    # Criar o solver
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Custos de transação com aumento de 500% nas rúpias
    custos = {
        ('Iene', 'Dólar'): 0.008,   
        ('Rúpia', 'Dólar'): 0.00016 * 5,  # Aumento de 500%
        ('Ringgit', 'Dólar'): 0.25   
    }

    # Definir variáveis de decisão
    iene_para_dolar = solver.IntVar(0.0, solver.infinity(), 'iene_para_dolar')
    rupia_para_dolar = solver.IntVar(0.0, solver.infinity(), 'rupia_para_dolar')
    ringgit_para_dolar = solver.IntVar(0.0, solver.infinity(), 'ringgit_para_dolar')

    # Função objetivo: Maximizar o valor total em dólares
    solver.Maximize(
        0.008 * iene_para_dolar + 0.00016 * 5 * rupia_para_dolar + 0.25 * ringgit_para_dolar
    )

    # Restrições de quantidade de cada moeda disponível
    solver.Add(iene_para_dolar <= 25000000)
    solver.Add(rupia_para_dolar <= 105000000)
    solver.Add(ringgit_para_dolar <= 28000000)

    # Resolver o problema
    status = solver.Solve()

    # Verificar o status da solução
    if status == pywraplp.Solver.OPTIMAL:
        print("Solução ótima com imposto de 500% sobre rúpias:")
        print(f"Ienes convertidos em dólares: {iene_para_dolar.solution_value()} dólares")
        print(f"Rúpias convertidas em dólares: {rupia_para_dolar.solution_value()} dólares")
        print(f"Ringgits convertidos em dólares: {ringgit_para_dolar.solution_value()} dólares")
        total_dolares = iene_para_dolar.solution_value() * 0.008 + rupia_para_dolar.solution_value() * 0.00016 * 5 + ringgit_para_dolar.solution_value() * 0.25
        print(f"Total em dólares após imposto: {total_dolares}")
    else:
        print("Não foi possível encontrar uma solução ótima.")

# Chamar a função para a parte (d)
com_imposto_de_500()
