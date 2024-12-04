from ortools.linear_solver import pywraplp

def fluxo_custo_minimo_d():
    # Inicializando o solver
    solver = pywraplp.Solver.CreateSolver('GLOP')
    
    # Dados do problema
    moedas = ['Iene', 'Rúpia', 'Ringgit']
    destino = 'Dólar'
    valores_iniciais = {'Iene': 15000000, 'Rúpia': 10500000000, 'Ringgit': 28000000}  # Valores em moedas locais
    taxas_cambio = {'Iene': 0.008, 'Rúpia': 0.00002, 'Ringgit': 0.2}  # Taxas de câmbio ajustadas
    limites = {'Iene': 1250000000, 'Rúpia': 5000000000, 'Ringgit': 20000000}  # Limites máximos por transação

    # Variáveis de decisão
    transacoes = {moeda: solver.NumVar(0, limites[moeda], f'transacao_{moeda}') for moeda in moedas}
    
    # Função objetivo: maximizar o valor convertido para dólares
    solver.Maximize(sum(transacoes[moeda] * taxas_cambio[moeda] for moeda in moedas))
    
    # Restrições de valor disponível
    for moeda in moedas:
        solver.Add(transacoes[moeda] <= valores_iniciais[moeda])
    
    # Resolver o problema
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        print('Solução ótima encontrada:')
        total_dolares = sum(transacoes[moeda].solution_value() * taxas_cambio[moeda] for moeda in moedas)
        for moeda in moedas:
            print(f"Converter {transacoes[moeda].solution_value()} de {moeda} para dólares.")
        print(f"Total convertido em dólares: {total_dolares}")
    else:
        print('Não foi possível encontrar uma solução.')

fluxo_custo_minimo_d()
