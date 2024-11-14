import plotly.graph_objects as go
import networkx as nx


def create_network(edges: list) -> tuple:
    graph = nx.Graph()
    graph.add_edges_from(edges)
    pos = nx.kamada_kawai_layout(graph, dim=3)
    x_nodes = [pos[node][0] for node in graph.nodes()]
    y_nodes = [pos[node][1] for node in graph.nodes()]
    z_nodes = [pos[node][2] for node in graph.nodes()]
    node_labels = list(graph.nodes())
    x_edges = []
    y_edges = []
    z_edges = []
    for edge in graph.edges():
        x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]
        z_edges += [pos[edge[0]][2], pos[edge[1]][2], None]
    return x_nodes, y_nodes, z_nodes, x_edges, y_edges, z_edges, node_labels


def create_plotly_plot(edges: list) -> go.Figure:
    x_nodes, y_nodes, z_nodes, x_edges, y_edges, z_edges, node_labels = create_network(edges)

    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=x_edges,
        y=y_edges,
        z=z_edges,
        mode='lines',
        line=dict(color='gray', width=2),
        hoverinfo='none'
    ))

    fig.add_trace(go.Scatter3d(
        x=x_nodes,
        y=y_nodes,
        z=z_nodes,
        mode='markers+text',
        marker=dict(size=8, color='skyblue', opacity=0.8),
        text=node_labels,
        textposition="top center",
        hoverinfo='text'
    ))

    fig.update_layout(
        title="3D Network Graph",
        showlegend=False,
        scene=dict(
            xaxis=dict(showbackground=False),
            yaxis=dict(showbackground=False),
            zaxis=dict(showbackground=False),
        ),
    )

    return fig
