stack = [node]
visited=set()
traversal_order = []

while stack:
    node = stack.pop()
    if node == target:
        break
    if node not in visited:
        visited.add(node)
        traversal_order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)

