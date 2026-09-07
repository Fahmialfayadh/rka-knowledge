from collections import deque

queue = deque([node])
visited = set()
traversal_order = []
while queue:
    node = queue.popleft()
    if node == target:
        break
    if node not in visited:
        visited.add(node)
        traversal_order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                queue.append(neighbor)



print(dir(queue))