from collections import defaultdict

from graphviz import Digraph

# ==================== KONFIGURASI PUZZLE ====================
START = [[0, 1, 3], [4, 2, 5], [7, 8, 6]]
GOAL = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
OUTPUT_FORMAT = "pdf"
MOVE_ORDER = {"Left": 0, "Up": 1, "Down": 2, "Right": 3}


def get_node_theme(node_type, on_solution):
    """Tema visual seragam untuk semua node."""
    if node_type == "goal":
        return {
            "frame_bg": "#D8F5D0",
            "accent": "#2B8A3E",
            "number_color": "#1B5E20",
        }
    if on_solution:
        return {
            "frame_bg": "#FFF3BF",
            "accent": "#C58B00",
            "number_color": "#7A5B00",
        }
    if node_type == "deadend":
        return {
            "frame_bg": "#FFE3E3",
            "accent": "#FA5252",
            "number_color": "#C92A2A",
        }
    return {
        "frame_bg": "#F1F3F5",
        "accent": "#495057",
        "number_color": "#1F2933",
    }


def state_to_html(state, number, node_type="normal", on_solution=False):
    """Buat HTML-like label dengan ukuran node yang konsisten."""
    theme = get_node_theme(node_type, on_solution)
    html = '<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="0">'
    html += (
        f'<TR><TD><FONT POINT-SIZE="18" COLOR="{theme["number_color"]}">'
        f'<B>{number}</B></FONT></TD></TR>'
    )
    html += (
        f'<TR><TD><TABLE BORDER="2" CELLBORDER="0" CELLSPACING="0" '
        f'CELLPADDING="5" BGCOLOR="{theme["frame_bg"]}" COLOR="{theme["accent"]}">'
        f'<TR><TD><TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" '
        f'CELLPADDING="0" COLOR="{theme["accent"]}">'
    )
    for row in state:
        html += "<TR>"
        for val in row:
            if val == 0:
                html += (
                    '<TD WIDTH="32" HEIGHT="32" BGCOLOR="black">'
                    '<FONT COLOR="black">0</FONT></TD>'
                )
            else:
                html += (
                    f'<TD WIDTH="32" HEIGHT="32" BGCOLOR="white">'
                    f'<FONT POINT-SIZE="15">{val}</FONT></TD>'
                )
        html += "</TR>"
    html += "</TABLE></TD></TR></TABLE></TD></TR></TABLE>>"
    return html


def build_tree_structure(nodes, edges):
    """Bangun struktur tree yang sudah terurut per arah move."""
    children_by_parent = defaultdict(list)
    for parent_id, child_id, move in edges:
        children_by_parent[parent_id].append((move, child_id))

    for parent_id in children_by_parent:
        children_by_parent[parent_id].sort(
            key=lambda item: (MOVE_ORDER.get(item[0], 99), int(item[1][1:]))
        )

    return children_by_parent


def compute_depth_order(nodes, edges):
    """Hitung depth tiap node + urutan kiri-kanan per depth."""
    if not nodes:
        return {}, {}

    children_by_parent = build_tree_structure(nodes, edges)
    depth_by_node = {}
    nodes_by_depth = defaultdict(list)

    def dfs(node_id, depth):
        depth_by_node[node_id] = depth
        nodes_by_depth[depth].append(node_id)
        for _, child_id in children_by_parent.get(node_id, []):
            dfs(child_id, depth + 1)

    dfs(nodes[0][0], 0)
    return depth_by_node, nodes_by_depth


def build_edge_attrs(move, is_solution_edge):
    """Atur edge agar lurus dan arah cabang konsisten."""
    attrs = {
        "label": f" {move} ",
        "fontsize": "10",
        "fontcolor": "#495057",
    }
    if move in ("Left", "Right"):
        attrs["minlen"] = "2"

    if is_solution_edge:
        attrs.update({
            "color": "green",
            "penwidth": "2.5",
            "fontcolor": "green",
        })

    return attrs


class TreeBuilder:
    def __init__(self):
        # Per-iterasi: list of (nodes, edges, solution_ids)
        self.iterations = []
        self.counter = 0  # penomoran kumulatif across all iterations

    def find_blank(self, state):
        for r in range(3):
            for c in range(3):
                if state[r][c] == 0:
                    return r, c

    def get_neighbors(self, state):
        neighbors = []
        r, c = self.find_blank(state)
        moves = [(-1, 0, "Up"), (1, 0, "Down"), (0, -1, "Left"), (0, 1, "Right")]
        for dr, dc, move_name in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_state = [row[:] for row in state]
                new_state[r][c], new_state[nr][nc] = new_state[nr][nc], new_state[r][c]
                neighbors.append((new_state, move_name))
        return neighbors

    def add_node(self, nodes, state, node_type="normal"):
        self.counter += 1
        node_id = f"n{self.counter}"
        nodes.append((node_id, [row[:] for row in state], self.counter, node_type))
        return node_id

    def dls(self, current, goal, depth, path, parent_id, nodes, edges, solution_ids):
        """DLS yang merecord semua node & edges."""
        node_id = self.add_node(nodes, current, "exploring")
        if parent_id is not None:
            move = path[-1][1] if path else ""
            edges.append((parent_id, node_id, move))

        if current == goal:
            nodes[-1] = (node_id, [row[:] for row in current], self.counter, "goal")
            solution_ids.add(node_id)
            return path, node_id

        if depth <= 0:
            nodes[-1] = (node_id, [row[:] for row in current], self.counter, "deadend")
            return None, None

        for neighbor, move in self.get_neighbors(current):
            if neighbor not in [p[0] for p in path]:
                result, goal_id = self.dls(
                    neighbor, goal, depth - 1,
                    path + [(neighbor, move)], node_id,
                    nodes, edges, solution_ids
                )
                if result is not None:
                    solution_ids.add(node_id)
                    return result, goal_id

        return None, None

    def solve_ids(self, max_depth=20):
        """IDS — record tree dari SEMUA iterasi dengan penomoran kumulatif."""
        for limit in range(max_depth):
            nodes = []
            edges = []
            solution_ids = set()

            result, goal_id = self.dls(
                START, GOAL, limit,
                [(START, "Start")], None,
                nodes, edges, solution_ids
            )

            self.iterations.append((limit, nodes, edges, solution_ids))
            node_count = len(nodes)

            if result is not None:
                print(f"Solusi ditemukan di depth limit {limit}")
                print(f"Nodes iterasi ini: {node_count}")
                print(f"Total nodes semua iterasi: {self.counter}")
                return result, limit

            print(f"Depth limit {limit}: {node_count} nodes, tidak ketemu")

        return None, None


def build_graph(iterations, title, graph_name):
    """Buat Graphviz Digraph dari sekumpulan iterasi IDS."""
    dot = Digraph(graph_name, format=OUTPUT_FORMAT, engine="dot")
    dot.attr(
        rankdir="TB",
        ordering="out",
        splines="polyline",
        bgcolor="white",
        fontname="Courier",
        dpi="180",
        pad="0.5",
    )
    dot.attr("node", shape="plaintext", fontname="Courier")
    dot.attr("edge", color="#333333", arrowsize="0.7")
    dot.attr(label=title,
             labelloc="t", fontsize="20", fontcolor="#333333")

    for limit, nodes, edges, solution_ids in iterations:
        depth_by_node, nodes_by_depth = compute_depth_order(nodes, edges)

        # Subgraph per iterasi
        with dot.subgraph(name=f"cluster_limit_{limit}") as sub:
            sub.attr(label=f"Depth Limit = {limit}", style="dashed",
                     color="#999999", fontsize="14", fontcolor="#666666",
                     margin="20")

            for node_id, state, number, node_type in nodes:
                label = state_to_html(
                    state,
                    number,
                    node_type=node_type,
                    on_solution=node_id in solution_ids,
                )
                sub.node(node_id, label=label)

            for depth, node_ids in sorted(nodes_by_depth.items()):
                with sub.subgraph(name=f"rank_limit_{limit}_{depth}") as rank_sub:
                    rank_sub.attr(rank="same")
                    for node_id in node_ids:
                        rank_sub.node(node_id)
                    for left_id, right_id in zip(node_ids, node_ids[1:]):
                        rank_sub.edge(left_id, right_id, style="invis", weight="200")

            for parent_id, child_id, move in sorted(
                edges,
                key=lambda edge: (
                    depth_by_node.get(edge[0], 0),
                    int(edge[0][1:]),
                    MOVE_ORDER.get(edge[2], 99),
                    int(edge[1][1:]),
                ),
            ):
                is_solution_edge = (
                    parent_id in solution_ids and child_id in solution_ids
                )
                sub.edge(parent_id, child_id, **build_edge_attrs(move, is_solution_edge))

    return dot


def render_grouped_graphs(builder):
    """Render IDS: satu iterasi satu file output."""
    rendered_files = []

    for limit, nodes, edges, solution_ids in builder.iterations:
        filename = f"ids_search_tree_{limit}"
        title = f"IDS Search Tree (Depth Limit {limit})"
        graph = build_graph([(limit, nodes, edges, solution_ids)], title, filename)
        output_path = graph.render(filename, directory=".", cleanup=True)
        rendered_files.append(output_path)

    return rendered_files


if __name__ == "__main__":
    builder = TreeBuilder()
    solution, depth = builder.solve_ids()

    if solution:
        output_paths = render_grouped_graphs(builder)
        print("\nSearch trees saved to:")
        for output_path in output_paths:
            print(f"- {output_path}")
        print(f"Solution path: {' -> '.join(m for _, m in solution)}")
    else:
        print("Solusi tidak ditemukan.")
