import networkx as nx
import matplotlib.pyplot as plt
import random

# Создаем граф с 10 узлами и соединяем каждый узел с двумя соседями
G = nx.Graph()
n_nodes = 10 # count of agents
G.add_nodes_from(range(n_nodes))
for i in range(n_nodes):
    G.add_edge(i, (i + 1) % n_nodes)
    G.add_edge(i, (i + 2) % n_nodes)

# Инициализируем доверие случайными значениями
for u, v in G.edges():
    G[u][v]['trust'] = random.random() #TODO how this get

# Функция для обновления доверия на основе взаимодействий агентов
def update_trust(G, iterations=100):
    for _ in range(iterations):
        u, v = random.sample(G.edges(), 1)[0]
        interaction_result = random.random() > 0.5
        trust_change = 0.1 if interaction_result else -0.1
        G[u][v]['trust'] = min(max(G[u][v]['trust'] + trust_change, 0), 1)

# Анализируем эмерджентное доверие в графе
update_trust(G)

# Визуализируем граф с помощью цвета и толщины ребер, основанных на доверии
pos = nx.circular_layout(G)
edge_colors = [G[u][v]['trust'] for u, v in G.edges()]
edge_widths = [G[u][v]['trust'] * 3 for u, v in G.edges()]
nx.draw(G, pos, node_size=500, node_color='blue', with_labels=True,
        edge_color=edge_colors, edge_cmap=plt.cm.Reds, width=edge_widths)
plt.show()
def emergent_trust(G):
    total_interaction_trust = 0
    for u, v in G.edges():
        total_interaction_trust += G[u][v]['interaction_count'] * G[u][v]['trust']

    emergent_trust = dict()
    for u, v in G.edges():
        emergent_trust[(u, v)] = (G[u][v]['interaction_count'] * G[u][v]['trust']) / total_interaction_trust

    return emergent_trust

# Создаем граф и инициализируем ребра с атрибутами 'interaction_count' и 'trust'
# G = nx.Graph()
# G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4)])
for u, v in G.edges():
    G[u][v]['interaction_count'] = random.randint(1, 10)
    # G[u][v]['trust'] = random.random()

# Вычисляем эмерджентное доверие
emergent_trust_values = emergent_trust(G)
print("Вычисляем эмерджентное доверие:")
print(emergent_trust_values)
def average_emergent_trust(G):
    emergent_trust_values = emergent_trust(G)
    total_emergent_trust = sum(emergent_trust_values.values())
    num_edges = len(G.edges())

    return total_emergent_trust / num_edges

# Вычисляем среднее эмерджентное доверие
average_ED = average_emergent_trust(G)
print("Среднее эмерджентное доверие:", average_ED)