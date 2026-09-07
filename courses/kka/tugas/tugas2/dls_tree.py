from graphviz import Digraph

# ==================== KONFIGURASI PUZZLE ====================
START = [[0, 1, 3], [4, 2, 5], [7, 8, 6]]
GOAL = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
DEPTH_LIMIT = 4
OUTPUT_FORMAT = "pdf"


def state_to_html(state, number, is_goal=False):
    """Buat HTML-like label untuk node Graphviz: tabel 3x3 + nomor."""
    bg = "#90EE90" if is_goal else "white"
    html = f'<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="3" BGCOLOR="{bg}">'
    html += f'<TR><TD COLSPAN="3" BORDER="0"><FONT POINT-SIZE="14"><B>{number}</B></FONT></TD></TR>'
    for row in state:
        html += "<TR>"
        for val in row:
            if val == 0:
                html += '<TD WIDTH="22" HEIGHT="22" BGCOLOR="black"><FONT COLOR="black">0</FONT></TD>'
            else:
                html += f'<TD WIDTH="22" HEIGHT="22">{val}</TD>'
        html += "</TR>"
    html += "</TABLE>>"
    return html


class TreeBuilder:
    def __init__(self):
        self.nodes = []       # (node_id, state, number, node_type)
        self.edges = []       # (parent_id, child_id, move)
        self.counter = 0
        self.solution_ids = set()

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

    def add_node(self, state, node_type="normal"):
        self.counter += 1
        node_id = f"n{self.counter}"
        self.nodes.append((node_id, [row[:] for row in state], self.counter, node_type))
        return node_id

    def dls(self, current, goal, depth, path, parent_id):
        """DLS yang merecord semua node & edges ke tree."""
        node_id = self.add_node(current, "exploring")
        if parent_id is not None:
            move = path[-1][1] if path else ""
            self.edges.append((parent_id, node_id, move))

        if current == goal:
            self.nodes[-1] = (node_id, [row[:] for row in current], self.counter, "goal")
            self.solution_ids.add(node_id)
            return path, node_id

        if depth <= 0:
            self.nodes[-1] = (node_id, [row[:] for row in current], self.counter, "deadend")
            return None, None

        for neighbor, move in self.get_neighbors(current):
            if neighbor not in [p[0] for p in path]:
                result, goal_id = self.dls(
                    neighbor, goal, depth - 1,
                    path + [(neighbor, move)], node_id
                )
                if result is not None:
                    self.solution_ids.add(node_id)
                    return result, goal_id

        return None, None

    def solve_dls(self, depth_limit):
        """Jalankan DLS sekali dengan depth limit tetap."""
        result, goal_id = self.dls(
            START, GOAL, depth_limit,
            [(START, "Start")], None
        )
        if result is not None:
            print(f"Solusi ditemukan dengan DLS (limit={depth_limit})")
            print(f"Total nodes: {len(self.nodes)}")
            return result
        else:
            print(f"DLS (limit={depth_limit}): {len(self.nodes)} nodes, solusi tidak ditemukan")
            return None


def build_graph(builder, depth_limit):
    """Buat Graphviz Digraph dari recorded tree."""
    dot = Digraph("DLS_Search_Tree", format=OUTPUT_FORMAT)
    dot.attr(
        rankdir="TB",
        ordering="out",
        splines="polyline",
        bgcolor="white",
        fontname="Courier",
        dpi="160",
        pad="0.4",
    )
    dot.attr("node", shape="plaintext", fontname="Courier")
    dot.attr("edge", color="#333333", arrowsize="0.7")
    dot.attr(nodesep="0.14", ranksep="1.0")
    dot.attr(label=f"DLS Search Tree (Depth Limit = {depth_limit})",
             labelloc="t", fontsize="20", fontcolor="#333333")

    for node_id, state, number, node_type in builder.nodes:
        is_goal = node_type == "goal"
        label = state_to_html(state, number, is_goal=is_goal)

        if node_id in builder.solution_ids:
            if is_goal:
                dot.node(node_id, label=label, style="filled",
                         fillcolor="#90EE90", penwidth="3", color="green")
            else:
                dot.node(node_id, label=label, style="filled",
                         fillcolor="#FFFF99", penwidth="2", color="#DAA520")
        elif node_type == "deadend":
            dot.node(node_id, label=label, style="filled",
                     fillcolor="#FFD0D0", penwidth="1", color="red")
        else:
            dot.node(node_id, label=label)

    for parent_id, child_id, move in builder.edges:
        if parent_id in builder.solution_ids and child_id in builder.solution_ids:
            dot.edge(parent_id, child_id, label=f" {move} ",
                     color="green", penwidth="2.5", fontcolor="green",
                     fontsize="10")
        else:
            dot.edge(parent_id, child_id, label=f" {move} ",
                     fontsize="9", fontcolor="#666666")

    return dot


if __name__ == "__main__":
    builder = TreeBuilder()
    solution = builder.solve_dls(DEPTH_LIMIT)

    if solution:
        graph = build_graph(builder, DEPTH_LIMIT).unflatten(stagger=4, fanout=True)
        output_path = graph.render("dls_search_tree", directory=".", cleanup=True)
        print(f"\nSearch tree saved to: {output_path}")
        print(f"Solution path: {' -> '.join(m for _, m in solution)}")
    else:
        print("Solusi tidak ditemukan.")
