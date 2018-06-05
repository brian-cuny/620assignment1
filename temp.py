from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import client

db = GraphDatabase('http://localhost:7474', username='neo4j', password='cosmic joke')

user = db.labels.create('User')
u1 = db.nodes.create(name='Marco')
user.add(u1)

q = 'MATCH (u:User) RETURN u'
results = db.query(q, returns=(client.Node, client.Node, str))
for r in results:
    print(r['name'])