from ortools.linear_solver import pywraplp

def com_imposto_de_500():
    # Criar o solver
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Custos de transação com aumento de 500% nas rúpias
    custos = {
        ('Iene', 'Dólar'): 0.008,  # Taxa de conversão de ienes para dólares
        ('Rúpia', 'Dólar'): 0.00016 * 5,  # Aumento de 500% nas rúpias
        ('Ringgit', 'Dólar'): 0.25   # Taxa de conversão de ringgits para dólares
    }

    # Definir variáveis de decisão: quanto de cada moeda será convertida para dólares
    iene_para_dolar = solver.IntVar(0.0, solver.infinity(), 'iene_para_dolar')
    rupia_para_dolar = solver.IntVar(0.0, solver.infinity(), 'rupia_para_dolar')
    ringgit_para_dolar = solver.IntVar(0.0, solver.infinity(), 'ringgit_para_dolar')

    # Função objetivo: Maximizar o valor total em dólares
    solver.Maximize(
        custos[('Iene', 'Dólar')] * iene_para_dolar + 
        custos[('Rúpia', 'Dólar')] * rupia_para_dolar + 
        custos[('Ringgit', 'Dólar')] * ringgit_para_dolar
    )

    # Restrições de quantidade de cada moeda disponível
    solver.Add(iene_para_dolar <= 25000000)  # Limite de ienes (25 milhões)
    solver.Add(rupia_para_dolar <= 105000000)  # Limite de rúpias (10,5 bilhões)
    solver.Add(ringgit_para_dolar <= 28000000)  # Limite de ringgits (28 milhões)

    # Resolver o problema
    status = solver.Solve()

    # Verificar o status da solução
    if status == pywraplp.Solver.OPTIMAL:
        print("Solução ótima com imposto de 500% sobre rúpias:")
        print(f"Ienes convertidos em dólares: {iene_para_dolar.solution_value()} dólares")
        print(f"Rúpias convertidas em dólares: {rupia_para_dolar.solution_value()} dólares")
        print(f"Ringgits convertidos em dólares: {ringgit_para_dolar.solution_value()} dólares")
        
        # Calcular o total em dólares após as transações
        total_dolares = (
            custos[('Iene', 'Dólar')] * iene_para_dolar.solution_value() + 
            custos[('Rúpia', 'Dólar')] * rupia_para_dolar.solution_value() + 
            custos[('Ringgit', 'Dólar')] * ringgit_para_dolar.solution_value()
        )
        print(f"Total em dólares após imposto de 500%: {total_dolares}")
    else:
        print("Não foi possível encontrar uma solução ótima.")

# Chamar a função para a parte (d)
com_imposto_de_500()
