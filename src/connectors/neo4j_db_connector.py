from neo4j import GraphDatabase

class Neo4jConnection:

    _instance = None

    def __init__(self):
        if Neo4jConnection._instance is None:
            Neo4jConnection._instance = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
        else:
            raise Exception("Attempting to create a second Neo4jConnection instance")

    @staticmethod
    def get_driver():
        if Neo4jConnection._instance is None: 
            Neo4jConnection()
        return Neo4jConnection._instance
