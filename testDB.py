from py2neo import neo4j

graph_db = neo4j.GraphDatabaseService()
a, b, ab = graph_db.create(node(name="Alice"), node(name="Bob"), rel(0, "KNOWS", 1))