import matplotlib.pyplot as plt
import networkx as nx
from ortools.graph import pywrapgraph



# Dados do problema
# Taxas de câmbio (valores em dólares)
exchange_rates = {
    'JPY': 0.008,    # 1 iene = 0.008 dólares
    'IDR': 0.00007,  # 1 rúpia = 0.00007 dólares
    'MYR': 0.22      # 1 ringgit = 0.22 dólares
}

# Custos de transação (em dólares)
transaction_costs = {
    'JPY': 0.001,    # custo por iene
    'IDR': 0.00002,  # custo por rúpia
    'MYR': 0.005     # custo por ringgit
}

# Limites máximos de conversão
max_limits = {
    'JPY': 15000000,       # 15 milhões de ienes
    'IDR': 10500000000,    # 10,5 bilhões de rúpias
    'MYR': 28000000        # 28 milhões de ringgits
}


# Modelo de fluxo de custo mínimo
def solve_currency_conversion(exchange_rates, transaction_costs, max_limits):
    # Criar solver de fluxo de custo mínimo
    min_cost_flow = pywrapgraph.SimpleMinCostFlow()
  # Alteração feita aqui

    # Definir nós e demandas
    start_nodes = []  # nós de origem
    end_nodes = []    # nós de destino
    capacities = []   # capacidades das arestas
    unit_costs = []   # custos unitários
    supplies = [0, 0, 0, 0]  # JPY, IDR, MYR, USD

    # Índices dos nós
    index_map = {'JPY': 0, 'IDR': 1, 'MYR': 2, 'USD': 3}
    for currency, rate in exchange_rates.items():
        start_nodes.append(index_map[currency])
        end_nodes.append(index_map['USD'])
        capacities.append(max_limits[currency])  # limite máximo
        cost_per_unit = (1 / rate) + transaction_costs[currency]
        unit_costs.append(int(cost_per_unit * 1000))  # Converter para inteiros

    # Nodo USD como demanda final
    supplies[index_map['USD']] = sum(max_limits.values())
    supplies[0] = -max_limits['JPY']
    supplies[1] = -max_limits['IDR']
    supplies[2] = -max_limits['MYR']

    # Adicionar arestas e capacidades ao modelo
    for i in range(len(start_nodes)):
        min_cost_flow.AddArcWithCapacityAndUnitCost(start_nodes[i], end_nodes[i], capacities[i], unit_costs[i])

    # Adicionar nós com suas demandas
    for i in range(len(supplies)):
        min_cost_flow.SetNodeSupply(i, supplies[i])

    # Resolver o problema
    if min_cost_flow.Solve() == min_cost_flow.OPTIMAL:
        result = {}
        for i in range(min_cost_flow.NumArcs()):
            if min_cost_flow.Flow(i) > 0:
                result[(start_nodes[i], end_nodes[i])] = min_cost_flow.Flow(i)
        return result, min_cost_flow.OptimalCost() / 1000  # Dividir para retornar ao valor original
    else:
        return None, None


# Resolver para o cenário com limites
result_with_limits, cost_with_limits = solve_currency_conversion(exchange_rates, transaction_costs, max_limits)

# Desenho da rede
def draw_network(exchange_rates, transaction_costs, max_limits):
    # Criar o grafo da rede
    G = nx.DiGraph()

    # Adicionar os nós
    nodes = ['JPY', 'IDR', 'MYR', 'USD']
    G.add_nodes_from(nodes)

    # Adicionar as arestas com capacidades e custos
    edges = [
        ('JPY', 'USD', {'capacity': max_limits['JPY'], 'cost': 1 / exchange_rates['JPY'] + transaction_costs['JPY']}),
        ('IDR', 'USD', {'capacity': max_limits['IDR'], 'cost': 1 / exchange_rates['IDR'] + transaction_costs['IDR']}),
        ('MYR', 'USD', {'capacity': max_limits['MYR'], 'cost': 1 / exchange_rates['MYR'] + transaction_costs['MYR']})
    ]
    G.add_edges_from(edges)

    # Desenhar o grafo
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 6))

    # Nós e arestas
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color='black')
    nx.draw_networkx_labels(G, pos, font_size=12, font_color='black', font_weight='bold')

    # Adicionar os rótulos das arestas com capacidade e custo
    edge_labels = {(u, v): f"cap={d['capacity']}, cost={d['cost']:.2f}" for u, v, d in edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

    # Exibir o grafo
    plt.title("Rede de Conversão de Moedas (Fluxo de Custo Mínimo)")
    plt.axis('off')
    plt.show()


# Desenhar a rede
draw_network(exchange_rates, transaction_costs, max_limits)

# Mostrar resultados
print(f"Resultado: {result_with_limits}")
print(f"Custo Total: {cost_with_limits}")
