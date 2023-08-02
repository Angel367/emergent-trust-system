import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import colors

from main import (EmergentTrust, read_agents_from_csv, generate_agents_from_kt,
                  generate_trusts_from_kt, read_trusts_from_csv, read_interactions_from_csv)


def draw_heatmap(agents, name_of_file):
    # data = np.random.randint(0, 100, size=(8, 8))
    #
    # Create a custom color map
    # with blue and green colors
    data = []
    for agent1 in agents:
        data1 = []
        for agent2 in agents:
            data2 = agent1.get_trust_score_by_id(agent2.ID)
            if data2:
                data1.append(data2.get_score())
            else:
                data1.append(0.5)
        data.append(data1)
    # print(data)
    hm = sns.heatmap(data=data,
                     annot=True,
                     cmap=colors.ListedColormap(
                       ["red", "orange", "yellow", "green"]
                     )
                     )

    # displaying the plotted heatmap
    plt.savefig("output/heapmap" + name_of_file)
    # Display the plot
    plt.show()


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
    print(G)
    # Инициализируем доверие случайными значениями
    # Анализируем эмерджентное доверие в графе
    # update_trust(G, interactions)
    max_int = max([u.get_interactions_by_id_count(v.ID) for u, v in G.edges()])
    if max_int == 0:
        max_int = 10
    # Визуализируем граф с помощью цвета и толщины ребер, основанных на доверии
    pos = nx.circular_layout(G)
    edge_widths = [8 * (u.get_interactions_by_id_count(v.ID) + 1) / max_int
                   for u, v in G.edges()]
    edge_colors = [(1 - G[u][v][0]['trust'], G[u][v][0]['trust'], 0) for u, v in G.edges()]
    node_colors = [((1 - v.get_reputation()), v.get_reputation(), 0) for v in G.nodes()]
    nx.draw(G, pos, node_size=500, node_color=node_colors, with_labels=True,
            edge_cmap=colors.ListedColormap(
                       ["red", "yellow", "green"]
                     ), edge_color=edge_colors, width=edge_widths,
            arrows=True, connectionstyle='arc3, rad = 0.1')
    plt.savefig("output/graph" + name_of_file)
    plt.show()


generate_agents_from_kt()
agents = read_agents_from_csv()
generate_trusts_from_kt(agents.__len__())
trusts = read_trusts_from_csv(agents)

draw_heatmap(agents, "1.png")
draw_graph(agents, "1.png")

read_interactions_from_csv(agents, 0, 3000)
draw_graph(agents, "2.png")
draw_heatmap(agents, "2.png")

read_interactions_from_csv(agents, 1000, 2000)
draw_graph(agents, "3.png")
draw_heatmap(agents, "3.png")

print("ET for 1 and 2", EmergentTrust.calculate_for_i_j(agents[0], agents[1], agents))
print("ET for 3 and 1", EmergentTrust.calculate_for_i_j(agents[2], agents[1], agents))
print("AET for sys", EmergentTrust.calculate_average(agents))
