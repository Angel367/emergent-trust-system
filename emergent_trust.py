# Import necessary libraries
from math import sqrt
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# Import functions and classes from the main module
from main import (
    EmergentTrust,
    read_agents_from_csv,
    generate_agents_from_kt,
    generate_trusts_from_kt,
    read_trusts_from_csv,
    read_interactions_from_csv,
)


# Function to draw a heatmap based on trust scores between agents
def draw_heatmap(agents, name_of_file):
    # Prepare the data for the heatmap based on trust scores
    data = []
    for agent1 in agents:
        data1 = []
        for agent2 in agents:
            data2 = agent1.get_trust_score_by_id(agent2.ID)
            if agent1 == agent2:
                data1.append(-1)  # Placeholder value for the diagonal (self-trust)
            elif data2:
                data1.append(data2.get_score())
            else:
                data1.append(0.5)  # Default value for missing trust scores
        data.append(data1)
    data = np.array(data)

    # Create the heatmap using seaborn and custom color map
    hm = sns.heatmap(
        data=data,
        annot=True,
        mask=data == -1,  # Hide the diagonal values (self-trust)
        cmap=LinearSegmentedColormap.from_list('red_green', ['r', 'y', 'g'], 256),
    )

    # Save the heatmap as an image
    plt.savefig("output/heapmap" + name_of_file)

    # Tweak the appearance of the plot
    plt.tick_params(
        axis='both',
        which='major',
        labelsize=10,
        labelbottom=False,
        bottom=False,
        top=False,
        labeltop=True,
    )

    # Display the plot
    plt.show()


# Function to draw a graph visualizing the trust relationships between agents
def draw_graph(agents, name_of_file):
    # Create a directed graph (digraph) and add nodes for each agent
    graph = nx.MultiDiGraph()
    graph.add_nodes_from(agents)

    # Add trust relationships (edges) between agents based on trust scores
    trusts = []
    for v in agents:
        for one in v.get_trust_scores():
            trusts.append(one)
    for trust in trusts:
        graph.add_edge(trust.get_agent1(), trust.get_agent2(), trust=trust.get_score())

    # Find the maximum interaction count for scaling edge widths
    max_int = max([u.get_interactions_by_id_count(v.ID) for u, v in graph.edges()])
    if max_int == 0:
        max_int = 10

    # Define the positions of nodes in a circular layout
    pos = nx.circular_layout(graph)

    # Set edge widths and colors based on interaction count and trust scores
    edge_widths = [5 * (u.get_interactions_by_id_count(v.ID) + 1) / max_int for u, v in graph.edges()]
    edge_colors = [
        (sqrt(1 - graph[u][v][0]['trust']), sqrt(graph[u][v][0]['trust']), 0) for u, v in graph.edges()
    ]

    # Set node colors based on reputation scores
    node_colors = [(sqrt(1 - v.get_reputation()), sqrt(v.get_reputation()), 0) for v in graph.nodes()]

    # Draw the graph using networkx and matplotlib
    nx.draw(
        graph,
        pos,
        node_size=500,
        node_color=node_colors,
        with_labels=True,
        edge_color=edge_colors,
        width=edge_widths,
        arrows=True,
        connectionstyle='arc3, rad = 0.1',
    )

    # Save the graph visualization as an image
    plt.savefig("output/graph" + name_of_file)

    # Display the plot
    plt.show()


# Generate agents data and read from CSV files
generate_agents_from_kt()
agents = read_agents_from_csv()
generate_trusts_from_kt(agents.__len__())
trusts = read_trusts_from_csv(agents)

# Draw the initial heatmap and graph
draw_heatmap(agents, "1.png")
draw_graph(agents, "1.png")

# Read interactions from CSV files and draw corresponding graph and heatmap
read_interactions_from_csv(agents, 0, 3)
draw_graph(agents, "2.png")
draw_heatmap(agents, "2.png")

read_interactions_from_csv(agents, 1, 2)
draw_graph(agents, "3.png")
draw_heatmap(agents, "3.png")

# Calculate and print emergent trust scores for specific agent pairs and the whole system
print("ET for 1 and 2", EmergentTrust.calculate_for_i_j(agents[0], agents[1], agents))
print("ET for 3 and 1", EmergentTrust.calculate_for_i_j(agents[2], agents[1], agents))
print("AET for sys", EmergentTrust.calculate_average(agents))
