import networkx as nx
import matplotlib.pyplot as plt

def desenhar_rede():
    # Criar o grafo direcionado
    G = nx.DiGraph()

    
    edges = [
        ("Iene", "Dólar", {"custo": 0.008, "limite": 1000000}),
        ("Rúpia", "Dólar", {"custo": 0.0001, "limite": 500000}),
        ("Ringgit", "Dólar", {"custo": 0.2, "limite": 300000}),
    ]

    # Adicionar arestas ao grafo
    for edge in edges:
        G.add_edge(edge[0], edge[1], **edge[2])

    # Layout para o grafo
    pos = nx.spring_layout(G)

    # Desenhar os nós e arestas
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=3000, font_size=10, font_weight="bold")
    
    # Adicionar rótulos com custo e limite nas arestas
    edge_labels = {(u, v): f'Custo={d["custo"]}\nLimite={d["limite"]}' for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    # Mostrar o grafo
    plt.title("Rede de Fluxo de Custo Mínimo")
    plt.show()

# Chamar a função para desenhar a rede
desenhar_rede()
