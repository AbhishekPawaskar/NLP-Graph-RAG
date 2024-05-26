from src.connectors.neo4j_db_connector import Neo4jConnection

driver = Neo4jConnection.get_driver()

def execute_graph_query(query_statement:str):
    try:
        records, summary, keys = driver.execute_query(query_statement)
        return str(records)
    except Exception as e:
        return None