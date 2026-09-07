from graph import *                                                              
                                                                                        
# Buat graf dari daftar edge
edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (2, 5)]                               
G = create_graph(edges)                                                                
print("Nodes:", list(G.nodes))
print("Edges:", list(G.edges))                                                         
                
# Cek degree node 2                                                                    
print("Degree node 2:", get_degree(G, 2))
                                                                                        
# DFS traversal dari node 1savefig
print("DFS dari node 1:", dfs_traversal(G, 1))                                         
                
# BFS traversal dari node 1                                                            
print("BFS dari node 1:", bfs_traversal(G, 1))
                                                                                        
# Shortest path dari node 1 ke 4
print("Shortest path 1 -> 4:", find_shortest_path(G, 1, 4))
                                                                                        
# Visualisasi dan export ke PNG
visualize_graph(G)                       