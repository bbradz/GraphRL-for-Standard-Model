import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Initialize the graph
G = nx.Graph()

# Define nodes and their types with descriptive labels
nodes = {
    "L+": {
        "type": "particle",
        "color": "blue",
        "shape": "D",
        "pos": (1, 2),
        "label": "Mass: M^{L+}\nCoupling: y^{+}_{L}\nCharge: 0\nSpin: 0",
    },
    "L0": {
        "type": "particle",
        "color": "blue",
        "shape": "D",
        "pos": (1, 0),
        "label": "Mass: M^{L0}\nCoupling: y^{0}_{L}\nCharge: 0\nSpin: 0",
    },
    "E+": {
        "type": "particle",
        "color": "blue",
        "shape": "D",
        "pos": (3, 2),
        "label": "Mass: M^{E+}\nCoupling: y^{+}_{E}\nCharge: ±1\nSpin: 1",
    },
    "E0": {
        "type": "particle",
        "color": "blue",
        "shape": "D",
        "pos": (3, 0),
        "label": "Mass: M^{E0}\nCoupling: y^{0}_{E}\nCharge: 0\nSpin: 1",
    },
    "λ^0_L, λ^+_L": {
        "type": "coupling",
        "color": "pink",
        "shape": "o",
        "pos": (0, 1),
        "label": "Coupling: λ^0_L, λ^+_L\nInteraction: g_1P_RF + g_2FP_R",
    },
    "λ^0_E, λ^+_E": {
        "type": "coupling",
        "color": "pink",
        "shape": "o",
        "pos": (4, 1),
        "label": "Coupling: λ^0_E, λ^+_E\nInteraction: g_1FP_R + g_2P_RF",
    },
    "y^+_{LE}, y^+_{EL}": {
        "type": "coupling",
        "color": "pink",
        "shape": "o",
        "pos": (2, 2),
        "label": "Coupling: y^+_{LE}, y^+_{EL}\nInteraction: g_1FP_R + g_2P_RF",
    },
    "y^0_{LE}, y^0_{EL}": {
        "type": "coupling",
        "color": "pink",
        "shape": "o",
        "pos": (2, 0),
        "label": "Coupling: y^0_{LE}, y^0_{EL}\nInteraction: g_1FP_R + g_2P_RF",
    },
}

# Add nodes to the graph
for node, attr in nodes.items():
    G.add_node(node, **attr)

# Define edges with styles
edges = [
    ("L+", "y^+_{LE}, y^+_{EL}", "solid"),
    ("y^+_{LE}, y^+_{EL}", "E+", "dashed"),
    ("L+", "λ^0_L, λ^+_L", "dashed"),
    ("λ^0_L, λ^+_L", "L0", "solid"),
    ("L0", "y^0_{LE}, y^0_{EL}", "solid"),
    ("y^0_{LE}, y^0_{EL}", "E0", "dashed"),
    ("E+", "λ^0_E, λ^+_E", "dashed"),
    ("λ^0_E, λ^+_E", "E0", "solid"),
]

# Add edges to the graph
for u, v, style in edges:
    G.add_edge(u, v, style=style)

# Define custom positions for the nodes
pos = {node: attr["pos"] for node, attr in nodes.items()}

# Draw nodes
for node, attr in G.nodes(data=True):
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=[node],
        node_color=attr["color"],
        node_shape="D" if attr["shape"] == "D" else "o",
        node_size=800,
        alpha=0.8,
    )

# Draw edges
for u, v, data in G.edges(data=True):
    nx.draw_networkx_edges(
        G, pos, edgelist=[(u, v)], style=data["style"], edge_color="black", alpha=0.8
    )

# Add labels for nodes
labels = {node: f"{node}\n{attr['label']}" for node, attr in G.nodes(data=True)}
nx.draw_networkx_labels(G, pos, labels=labels, font_size=7, font_color="black")

# Create legend elements
legend_elements = [
    Line2D([0], [0], marker="D", color="w", label="Particle Node", markerfacecolor="blue", markersize=8),
    Line2D([0], [0], marker="o", color="w", label="Coupling Node", markerfacecolor="pink", markersize=8),
    Line2D([0], [0], color="black", lw=1.5, label="Edge Type: e1 (Solid Line)", linestyle="solid"),
    Line2D([0], [0], color="black", lw=1.5, label="Edge Type: e2 (Dashed Line)", linestyle="dashed"),
]

# Add legend to the plot
plt.legend(
    handles=legend_elements,
    loc="lower center",
    bbox_to_anchor=(0.5, -0.15),
    ncol=2,
    fontsize=8,
    frameon=False,
)

# Display the graph
plt.title("Graph Network of BSM Fermions and Couplings (Undirected)", fontsize=10)
plt.tight_layout()
plt.axis("off")
plt.show()
