import networkx as nx
from collections import deque
def create_graph(edges: list[tuple[int, int]]) -> nx.Graph:
    """Membuat graph dari daftar edge.

    Args:
        edges: Daftar edge, di mana setiap edge adalah tuple (node1, node2).

    Returns:
        Graph yang dibuat dari daftar edge.
    """
    graph = nx.Graph()
    graph.add_edges_from(edges)
    return graph

def get_degree(graph: nx.Graph, node: int) -> int:
    """Menghitung derajat dari sebuah node dalam graph.

    Args:
        graph: Graph yang akan dihitung derajatnya.
        node: Node yang akan dihitung derajatnya.

    Returns:
        Derajat dari node tersebut.
    """
    return graph.degree[node]

def dfs_traversal(graph: nx.Graph, start_node: int) -> list[int]:
    """Melakukan traversal DFS pada graph.

    Args:
        graph: Graph yang akan ditraversal.
        start_node: Node awal untuk traversal.

    Returns:
        Daftar node yang dikunjungi selama traversal DFS.
    """
    return list(nx.dfs_preorder_nodes(graph, source=start_node))
    

def bfs_traversal(graph: nx.Graph, start_node: int) -> list[int]:
    """Melakukan traversal BFS pada graph.

    Args:
        graph: Graph yang akan ditraversal.
        start_node: Node awal untuk traversal.

    Returns:
        Daftar node yang dikunjungi selama traversal BFS.
    """
 
    return list(nx.bfs_tree(graph, source=start_node).nodes())

def find_shortest_path(graph: nx.Graph, start_node: int, end_node: int) -> list[int]:
    """Mencari jalur terpendek antara dua node dalam graph.

    Args:
        graph: Graph yang akan dicari jalur terpendeknya.
        start_node: Node awal untuk pencarian.
        end_node: Node tujuan untuk pencarian.

    Returns:
        Daftar node yang membentuk jalur terpendek dari start_node ke end_node.
    """
    try:
        return nx.shortest_path(graph, source=start_node, target=end_node)
    except nx.NetworkXNoPath:
        return []  # return daftar kosong jika tidak ada jalur antara kedua node
    
def visualize_graph(graph: nx.Graph) -> None:
    """Visualisasi graph menggunakan Matplotlib.

    Args:
        graph: Graph yang akan divisualisasikan.
    """
    import matplotlib.pyplot as plt
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray')
    plt.savefig('graph.png')