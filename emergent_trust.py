import datetime

import networkx as nx
import matplotlib.pyplot as plt
import random

from main import Agent, Trust, Interaction


# Функция для обновления доверия на основе взаимодействий агентов
# def update_trust(G, iterations):
#     for interaction in iterations:
#         u = interaction.get_agent1()
#         v = interaction.get_agent2()
#
#         interaction_result = interaction.get_sentiment() * \
#             interaction.get_interaction_type() * u.reputation * v.reputation
#         trust_change = 0.1 if interaction_result else -0.1
#         G[u][v]['trust'] = min(max(G[u][v]['trust'] + trust_change, 0), 1)


def draw_graph(agents, trusts):
    # Создаем граф с 10 узлами и соединяем каждый узел с двумя соседями
    G = nx.MultiDiGraph()
    G.add_nodes_from(agents)
    for trust in trusts:
        G.add_edge(trust.get_agent1(),
                   trust.get_agent2(), trust=trust.get_score())
    edge_widths = []
    # Инициализируем доверие случайными значениями


    # Анализируем эмерджентное доверие в графе
    # update_trust(G, interactions)
    # Визуализируем граф с помощью цвета и толщины ребер, основанных на доверии
    pos = nx.circular_layout(G)
    edge_widths = [u.get_interactions_by_id_count(v.ID) + 1 for u, v in G.edges()]
    edge_colors = [(1 - G[u][v][0]['trust'], G[u][v][0]['trust'], 0) for u, v in G.edges()]
    print(edge_widths)
    node_colors = [((1-v.get_reputation()), v.get_reputation(), 0) for v in G.nodes()]
    # print(node_colors)
    nx.draw(G, pos, node_size=500, node_color=node_colors, with_labels=True,
           edge_cmap=plt.cm.Reds, edge_color=edge_colors, width=edge_widths,
            arrows=True, connectionstyle='arc3, rad = 0.1')
    plt.show()


agents = [Agent(1),
          Agent(2, "123", 0.95),
          Agent(3, "qwe", 0.1)
          ]
trusts = [
    Trust(agents[1], agents[0], 0.5),
    Trust(agents[0], agents[2], 0.9),
    Trust(agents[2], agents[1], 0.1),
    Trust(agents[0], agents[1], 0.7)
          ]
interactions = [
    Interaction(agents[0], agents[1], -0.9, 1, datetime.datetime.now()),
    Interaction(agents[0], agents[1], -0.8, 0.6, datetime.datetime.now()),
    Interaction(agents[0], agents[1], -0.7, 1, datetime.datetime.now()),
    Interaction(agents[0], agents[1], -0.7, 0.5, datetime.datetime.now()),
    Interaction(agents[0], agents[1], -0.9, 1, datetime.datetime.now()),
    Interaction(agents[0], agents[1], -0.9, 1, datetime.datetime.now())
]
draw_graph(agents, trusts)

# def emergent_trust(G):
#     total_interaction_trust = 0
#     for u, v in G.edges():
#         total_interaction_trust += G[u][v]['interaction_count'] * G[u][v]['trust']
#
#     emergent_trust = dict()
#     for u, v in G.edges():
#         emergent_trust[(u, v)] = (G[u][v]['interaction_count'] * G[u][v]['trust']) / total_interaction_trust
#
#     return emergent_trust

# # Создаем граф и инициализируем ребра с атрибутами 'interaction_count' и 'trust'
# # G = nx.Graph()
# # G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4)])
# for u, v in G.edges():
#     G[u][v]['interaction_count'] = random.randint(1, 10)
#     # G[u][v]['trust'] = random.random()
#
# # Вычисляем эмерджентное доверие
# emergent_trust_values = emergent_trust(G)
# print("Вычисляем эмерджентное доверие:")
# print(emergent_trust_values)
# def average_emergent_trust(G):
#     emergent_trust_values = emergent_trust(G)
#     total_emergent_trust = sum(emergent_trust_values.values())
#     num_edges = len(G.edges())
#
#     return total_emergent_trust / num_edges
#
# # Вычисляем среднее эмерджентное доверие
# average_ED = average_emergent_trust(G)
# print("Среднее эмерджентное доверие:", average_ED)