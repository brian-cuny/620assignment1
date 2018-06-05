from neo4j.v1 import GraphDatabase
from igraph import Graph as iGraph
from igraph import plot
import csv


class BeachHead(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def delete(self):
        with self._driver.session() as session:
            session.run('MATCH (n) DETACH DELETE n')
            session.run('CREATE CONSTRAINT ON (p:Person) ASSERT p.name IS UNIQUE')

    def add_person(self, name):
        with self._driver.session() as session:
            session.run("MERGE (:Person {name: $name})", name=name)

    def add_relationship(self, a, b):
        with self._driver.session() as session:
            session.run('MERGE (a:Person {name: $a})'
                        'MERGE (b:Person {name: $b})'
                        'CREATE (a)-[:KNOWS]->(b)'
                        'CREATE (b)-[:KNOWS]->(a)', a=a, b=b)

    def query(self, query):
        with self._driver.session() as session:
            return session.run(query)


if __name__ == '__main__':
    neo = BeachHead('bolt://localhost:7687', 'neo4j', 'cosmic joke')
    neo.delete()

    with open('relationships.csv', newline='') as csvfile:
        for r in csv.reader(csvfile, delimiter=','):
            neo.add_relationship(r[0], r[1])

    results = [(n1, n2) for n1, n2 in neo.query('MATCH (p:Person)-[:KNOWS]->(p2:Person) '
                                                'WHERE p.name < p2.name '
                                                'RETURN p.name, p2.name '
                                                'ORDER BY p.name, p2.name'
                                                )
               ]

    for n1, n2 in results:
        print(f'{n1} KNOWS {n2}')

    ig = iGraph.TupleList(results, vertex_name_attr='label')
    plot(ig)



