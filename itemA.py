import matplotlib.pyplot as plt
import networkx as nx

def desenhar_rede():
    """
    Desenha a rede de fluxo de custo mínimo para o problema.
    """
    # Criar o grafo
    G = nx.DiGraph()

    # Adicionar os nós
    moedas = ['Ienes', 'Rúpias', 'Ringgits', 'Dólares']
    G.add_nodes_from(moedas)

    # Adicionar as arestas com capacidades e custos
    arestas = [
        ('Ienes', 'Dólares', {'capacidade': 25000000, 'custo': 0.008}),
        ('Rúpias', 'Dólares', {'capacidade': 105000000, 'custo': 0.00016}),
        ('Ringgits', 'Dólares', {'capacidade': 28000000, 'custo': 0.25})
    ]

    G.add_edges_from([(u, v, d) for u, v, d in arestas])

    # Configurar posições para o desenho
    pos = nx.spring_layout(G)

    # Desenhar nós, arestas e rótulos
    plt.figure(figsize=(10, 8))
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color='black')
    nx.draw_networkx_labels(G, pos, font_size=12, font_color='black')

    # Adicionar rótulos às arestas com capacidade e custo
    edge_labels = {(u, v): f"Cap: {d['capacidade']}, Custo: {d['custo']}" for u, v, d in arestas}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

    # Título e exibição
    plt.title("Rede de Fluxo de Custo Mínimo")
    plt.axis('off')
    plt.show()


desenhar_rede()