import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Initialize the graph
G = nx.Graph()

# Define nodes: Particles and Coupling/Interaction terms
nodes = {
    # Fermions: First generation
    "u": {"type": "particle", "color": "blue", "shape": "D", "pos": (1, 6), "label": "Quark u\nCharge: +2/3\nSpin: 1/2"},
    "d": {"type": "particle", "color": "blue", "shape": "D", "pos": (1, 4), "label": "Quark d\nCharge: -1/3\nSpin: 1/2"},
    "e-": {"type": "particle", "color": "green", "shape": "D", "pos": (1, 2), "label": "Electron\nCharge: -1\nSpin: 1/2"},
    "νe": {"type": "particle", "color": "green", "shape": "D", "pos": (1, 0), "label": "Electron Neutrino\nCharge: 0\nSpin: 1/2"},
    # Fermions: Second generation
    "c": {"type": "particle", "color": "blue", "shape": "D", "pos": (3, 6), "label": "Quark c\nCharge: +2/3\nSpin: 1/2"},
    "s": {"type": "particle", "color": "blue", "shape": "D", "pos": (3, 4), "label": "Quark s\nCharge: -1/3\nSpin: 1/2"},
    "μ-": {"type": "particle", "color": "green", "shape": "D", "pos": (3, 2), "label": "Muon\nCharge: -1\nSpin: 1/2"},
    "νμ": {"type": "particle", "color": "green", "shape": "D", "pos": (3, 0), "label": "Muon Neutrino\nCharge: 0\nSpin: 1/2"},
    # Fermions: Third generation
    "t": {"type": "particle", "color": "blue", "shape": "D", "pos": (5, 6), "label": "Quark t\nCharge: +2/3\nSpin: 1/2"},
    "b": {"type": "particle", "color": "blue", "shape": "D", "pos": (5, 4), "label": "Quark b\nCharge: -1/3\nSpin: 1/2"},
    "τ-": {"type": "particle", "color": "green", "shape": "D", "pos": (5, 2), "label": "Tau\nCharge: -1\nSpin: 1/2"},
    "ντ": {"type": "particle", "color": "green", "shape": "D", "pos": (5, 0), "label": "Tau Neutrino\nCharge: 0\nSpin: 1/2"},
    # Bosons
    "γ": {"type": "particle", "color": "red", "shape": "o", "pos": (7, 5), "label": "Photon\nCharge: 0\nSpin: 1"},
    "W+": {"type": "particle", "color": "purple", "shape": "o", "pos": (7, 3), "label": "W Boson\nCharge: +1\nSpin: 1"},
    "Z0": {"type": "particle", "color": "purple", "shape": "o", "pos": (7, 1), "label": "Z Boson\nCharge: 0\nSpin: 1"},
    "g": {"type": "particle", "color": "orange", "shape": "o", "pos": (9, 3), "label": "Gluon\nCharge: 0\nSpin: 1"},
    "H": {"type": "particle", "color": "yellow", "shape": "o", "pos": (11, 3), "label": "Higgs Boson\nCharge: 0\nSpin: 0"},
    # Interaction Terms
    "EM Interaction": {"type": "interaction", "color": "pink", "shape": "o", "pos": (4, 5), "label": "Electromagnetic\nL = - e jμ Aμ\nFeature: {e}"},
    "Weak Interaction": {"type": "interaction", "color": "pink", "shape": "o", "pos": (4, 3), "label": "Weak\nL = g_W JμWμ\nFeature: {g_W}"},
    "Strong Interaction": {"type": "interaction", "color": "pink", "shape": "o", "pos": (8, 3), "label": "Strong\nL = g_s JμAμ\nFeature: {g_s}"},
    "Yukawa Coupling": {"type": "interaction", "color": "pink", "shape": "o", "pos": (10, 3), "label": "Higgs\nL = - λψHψ\nFeature: {λψH}"},
}

# Add nodes to the graph
for node, attr in nodes.items():
    G.add_node(node, **attr)

# Define edges with styles and labels representing interactions
edges = [
    # Electromagnetic interaction
    ("e-", "EM Interaction", "solid", "F->Coupling: e F"),
    ("u", "EM Interaction", "solid", "F->Coupling: e F"),
    ("d", "EM Interaction", "solid", "F->Coupling: e F"),
    ("EM Interaction", "γ", "solid", "Coupling->F: e F"),
    # Weak interaction
    ("νe", "Weak Interaction", "dashed", "F->Coupling: g_W J"),
    ("e-", "Weak Interaction", "dashed", "F->Coupling: g_W J"),
    ("u", "Weak Interaction", "dashed", "F->Coupling: g_W J"),
    ("Weak Interaction", "W+", "dashed", "Coupling->F: g_W J"),
    ("Weak Interaction", "Z0", "dashed", "Coupling->F: g_W J"),
    # Strong interaction
    ("u", "Strong Interaction", "solid", "F->Coupling: g_s J"),
    ("d", "Strong Interaction", "solid", "F->Coupling: g_s J"),
    ("g", "Strong Interaction", "solid", "Coupling->F: g_s J"),
    # Yukawa coupling (Higgs)
    ("H", "Yukawa Coupling", "solid", "H->Coupling: λψH"),
    ("u", "Yukawa Coupling", "solid", "F->Coupling: λψH"),
    ("d", "Yukawa Coupling", "solid", "F->Coupling: λψH"),
    ("e-", "Yukawa Coupling", "solid", "F->Coupling: λψH"),
]

# Add edges to the graph
for u, v, style, label in edges:
    G.add_edge(u, v, style=style, label=label)

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

# Draw edges with labels
for u, v, data in G.edges(data=True):
    nx.draw_networkx_edges(
        G, pos, edgelist=[(u, v)], style=data["style"], edge_color="black", alpha=0.8
    )
    edge_pos = ((pos[u][0] + pos[v][0]) / 2, (pos[u][1] + pos[v][1]) / 2)
    plt.text(edge_pos[0], edge_pos[1], data["label"], fontsize=6, color="black", alpha=0.9)

# Add labels for nodes
labels = {node: f"{node}\n{attr['label']}" for node, attr in G.nodes(data=True)}
nx.draw_networkx_labels(G, pos, labels=labels, font_size=7, font_color="black")

# Create legend elements
legend_elements = [
    Line2D([0], [0], marker="D", color="w", label="Fermion Node", markerfacecolor="blue", markersize=8),
    Line2D([0], [0], marker="D", color="w", label="Lepton Node", markerfacecolor="green", markersize=8),
    Line2D([0], [0], marker="o", color="w", label="Boson Node", markerfacecolor="red", markersize=8),
    Line2D([0], [0], marker="o", color="w", label="Interaction Node", markerfacecolor="pink", markersize=8),
    Line2D([0], [0], color="black", lw=1.5, label="Interaction (Solid Line)", linestyle="solid"),
    Line2D([0], [0], color="black", lw=1.5, label="Interaction (Dashed Line)", linestyle="dashed"),
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
plt.title("Graph Network of the Standard Model of Physics with Interactions", fontsize=10)
plt.tight_layout()
plt.axis("off")
plt.show()
