from neo4j.v1 import GraphDatabase
import csv
import networkx as nx
import matplotlib.pyplot as plt


class BeachHead(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def delete(self):
        with self._driver.session() as session:
            session.run('MATCH (n) DETACH DELETE n')
            session.run('CREATE CONSTRAINT ON (p:Person) ASSERT p.name IS UNIQUE')

    def add_relationship(self, a, b, rel):
        with self._driver.session() as session:
            session.run('MERGE (a:Person {name: $a})'
                        'MERGE (b:Person {name: $b})'
                        'CREATE (a)-[k:KNOWS]->(b)'
                        'SET k.type = {type}'
                        'CREATE (b)-[l:KNOWS]->(a)'
                        'SET l.type = {rel}', a=a, b=b, rel=rel)

    def query(self, query):
        with self._driver.session() as session:
            return session.run(query)


if __name__ == '__main__':
    neo = BeachHead('bolt://localhost:7687', 'cuny', 'password')
    neo.delete()

    with open('relationships.csv', newline='') as csvfile:
        for r in csv.reader(csvfile, delimiter=','):
            neo.add_relationship(r[0], r[1], r[2])

    results = [(n1, n2, {'rel': k}) for n1, n2, k in neo.query('MATCH (p:Person)-[k:KNOWS]->(p2:Person) '
                                                               'WHERE p.name < p2.name '
                                                               'RETURN p.name, p2.name, k.type '
                                                               'ORDER BY p.name, p2.name'
                                                              )
               ]
    neo.close()

    for n1, n2, k in results:
        print(f'{n1} {k["rel"]} {n2}')

    G = nx.Graph()
    G.add_edges_from(results)
    pos = nx.spring_layout(G)
    nx.draw(G, with_labels=True, font_weight='bold', pos=pos)
    edge_labels = dict([((u, v), d['rel']) for u, v, d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels = edge_labels)
    plt.show()



