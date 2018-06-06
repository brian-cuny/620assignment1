results = [(n1, n2, {'rel': k}) for n1, n2, k in 
                neo.query('MATCH (p:Person)-[k:KNOWS]->(p2:Person) '
                          'WHERE p.name < p2.name '
                          'RETURN p.name, p2.name, k.type '
                          'ORDER BY p.name, p2.name'
                         )
               ]
neo.close()
G = nx.Graph()
G.add_edges_from(results)
pos = nx.spring_layout(G)
nx.draw(G, with_labels=True, font_weight='bold', pos=pos)
edge_labels = dict([((u, v), d['rel']) for u, v, d in G.edges(data=True)])
nx.draw_networkx_edge_labels(G, pos=pos, edge_labels = edge_labels)
plt.show()