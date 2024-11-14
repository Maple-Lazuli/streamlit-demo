import plotly.graph_objects as go
import networkx as nx


def create_network(edges: list, label_team_only: bool = False, selected_member: str = None) -> tuple:
    graph = nx.Graph()
    graph.add_edges_from(edges)
    pos = nx.kamada_kawai_layout(graph, dim=3)
    x_nodes = [pos[node][0] for node in graph.nodes()]
    y_nodes = [pos[node][1] for node in graph.nodes()]
    z_nodes = [pos[node][2] for node in graph.nodes()]

    hover_text = list(graph.nodes())
    if label_team_only:
        team_names = set([edge[0] for edge in edges])
        node_labels = [node if node in team_names else None for node in graph.nodes()]
    else:
        node_labels = list(graph.nodes())

    node_colors = []

    if selected_member is not None:
        selected_node = selected_member
        neighbors = set(graph.neighbors(selected_node))

        for node in graph.nodes():
            if node == selected_node:
                node_colors.append("red")
            elif node in neighbors:
                node_colors.append("red")
            else:
                node_colors.append("grey")
    else:
        for node in graph.nodes():
            node_colors.append("grey")

    x_edges = []
    y_edges = []
    z_edges = []
    for edge in graph.edges():
        x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]
        z_edges += [pos[edge[0]][2], pos[edge[1]][2], None]
    return x_nodes, y_nodes, z_nodes, x_edges, y_edges, z_edges, node_labels, node_colors, hover_text


def create_plotly_plot(edges: list) -> go.Figure:
    x_nodes, y_nodes, z_nodes, x_edges, y_edges, z_edges, node_labels, \
        node_colors , hover_text = create_network(edges)

    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=x_edges,
        y=y_edges,
        z=z_edges,
        mode='lines',
        line=dict(color='gray', width=1),
        opacity=0.4,
        hoverinfo='none'
    ))

    fig.add_trace(go.Scatter3d(
        x=x_nodes,
        y=y_nodes,
        z=z_nodes,
        mode='markers+text',
        marker=dict(size=8, color=node_colors, opacity=0.4),
        text=node_labels,
        textposition="top center",
        hovertext=hover_text,
        hoverinfo='text'
    ))

    fig.update_layout(
        title="3D Network Graph",
        showlegend=False,
        scene=dict(
            xaxis=dict(showgrid=False, zeroline=False, showbackground=False, visible=False),
            yaxis=dict(showgrid=False, zeroline=False, showbackground=False, visible=False),
            zaxis=dict(showgrid=False, zeroline=False, showbackground=False, visible=False),
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        dragmode="orbit"
    )

    return fig
