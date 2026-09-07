import graph as g


def test_graph_creation():
    edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (2, 5)]
    graph = g.create_graph(edges)
    assert len(graph.nodes) == 5
    assert len(graph.edges) == 6


def test_get_degree():
    graph = g.create_graph([(1, 2), (2, 3), (3, 4)])
    assert g.get_degree(graph, 2) == 2


def test_dfs_traversal():
    graph = g.create_graph([(1, 2), (2, 3), (3, 4)])
    assert g.dfs_traversal(graph, 1) == [1, 2, 3, 4]


def test_bfs_traversal():
    graph = g.create_graph([(1, 2), (1, 3), (3, 4)])
    assert g.bfs_traversal(graph, 1) == [1, 2, 3, 4]


def test_shortest_path():
    graph = g.create_graph([(1, 2), (2, 3), (3, 4)])
    assert g.find_shortest_path(graph, 1, 4) == [1, 2, 3, 4]