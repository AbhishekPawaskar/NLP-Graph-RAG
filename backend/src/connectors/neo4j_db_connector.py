import os
from neo4j import GraphDatabase

class Neo4jConnection:

    _instance = None

    def __init__(self):
        if Neo4jConnection._instance is None:
            Neo4jConnection._instance = GraphDatabase.driver(os.environ.get('GRAPH_DB_URL'), auth=(os.environ.get('GRAPH_DB_USERNAME'), os.environ.get('GRAPH_DB_PASSWORD')))
        else:
            raise Exception("Attempting to create a second Neo4jConnection instance")

    @staticmethod
    def get_driver():
        if Neo4jConnection._instance is None: 
            Neo4jConnection()
        return Neo4jConnection._instance
