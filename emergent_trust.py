import datetime
import networkx as nx
import matplotlib.pyplot as plt
from main import Interaction, EmergentTrust, read_agents_from_csv, \
    generate_agents_from_kt, generate_trusts_from_kt, read_trusts_from_csv, read_interactions_from_csv


def draw_graph(agents, name_of_file):
    # Создаем граф с 10 узлами и соединяем каждый узел с двумя соседями
    G = nx.MultiDiGraph()
    G.add_nodes_from(agents)
    trusts = []
    for v in agents:
        for one in v.get_trust_scores():
            trusts.append(one)
    # print(trusts)
    for trust in trusts:
        # print(trust)
        G.add_edge(trust.get_agent1(),
                   trust.get_agent2(), trust=trust.get_score())
    edge_widths = []
    print(G)
    # Инициализируем доверие случайными значениями
    # Анализируем эмерджентное доверие в графе
    # update_trust(G, interactions)
    # Визуализируем граф с помощью цвета и толщины ребер, основанных на доверии
    pos = nx.circular_layout(G)
    edge_widths = [u.get_interactions_by_id_count(v.ID) + 1 for u, v in G.edges()]
    edge_colors = [(1 - G[u][v][0]['trust'], G[u][v][0]['trust'], 0) for u, v in G.edges()]
    # print(edge_widths)
    node_colors = [((1 - v.get_reputation()), v.get_reputation(), 0) for v in G.nodes()]
    # print(node_colors)
    nx.draw(G, pos, node_size=500, node_color=node_colors, with_labels=True,
            edge_cmap=plt.cm.Reds, edge_color=edge_colors, width=edge_widths,
            arrows=True, connectionstyle='arc3, rad = 0.1')
    plt.savefig(name_of_file)
    plt.show()

generate_agents_from_kt()
agents = read_agents_from_csv()
generate_trusts_from_kt(agents.__len__())
trusts = read_trusts_from_csv(agents)
print(f"trusts:{trusts}")
draw_graph(agents, "1.png")
# read_interactions_from_csv(agents, 0, 100)
draw_graph(agents, "2.png")
# read_interactions_from_csv(agents, 10, 20)
draw_graph(agents, "3.png")


# agents = [Agent(1),
#           Agent(2, "123", 0.95),
#           Agent(3, "qwe", 0.1)
#           ]

# trusts = [
#     Trust(agents[1], agents[0], 0.5),
#     Trust(agents[0], agents[2], 0.9),
#     Trust(agents[2], agents[1], 0.1),
#     Trust(agents[0], agents[1], 0.7)
# ]

#
# Interaction(agents[1], agents[2], 0.9, 1, datetime.datetime.now())
# Interaction(agents[0], agents[1], -0.9, 1, datetime.datetime.now())
# Interaction(agents[1], agents[0], -0.8, 0.6, datetime.datetime.now())
# Interaction(agents[2], agents[1], 0.7, 1, datetime.datetime.now())
# Interaction(agents[0], agents[2], 0.7, 0.5, datetime.datetime.now())
#
# interactions = [
#     Interaction(agents[1], agents[2], 0.9, 1, datetime.datetime.now()),
#     Interaction(agents[2], agents[0], -0.9, 1, datetime.datetime.now()),
#     Interaction(agents[2], agents[0], -0.8, 0.6, datetime.datetime.now()),
#     Interaction(agents[0], agents[1], -0.7, 1, datetime.datetime.now()),
#     Interaction(agents[0], agents[1], -0.7, 0.5, datetime.datetime.now()),
#     Interaction(agents[2], agents[1], 0.9, 1, datetime.datetime.now()),
#     Interaction(agents[2], agents[1], 0.9, 1, datetime.datetime.now()),
#     Interaction(agents[0], agents[2], -0.9, 1, datetime.datetime.now()),
#     Interaction(agents[0], agents[2], -0.9, 1, datetime.datetime.now())
# ]


print("ET for 1 and 2", EmergentTrust.calculate_for_i_j(agents[0], agents[1], agents))
print("ET for 3 and 1", EmergentTrust.calculate_for_i_j(agents[2], agents[1], agents))
print("AET for sys", EmergentTrust.calculate_average(agents))
