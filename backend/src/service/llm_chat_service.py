import re
import pydantic
from src.connectors.llm_connector import LLMConnection

class ChatService:
    def __init__(self):
        self.client = LLMConnection().client
        self.graph_schema =  """Nodes and their properties are the following:
                            {'label': 'MOVIE', 'properties': ['name', 'overview', 'cast']}
                            {'labels': 'GENRE','properties': ['name']}
                            {'labels': 'LANGUAGE','properties': ['name']}


                            The relationships are the following:
                            {'source': 'MOVIE', 'relationship': 'GENRE', 'target': 'GENRE'} #A Movie can be connected to many Genres
                            {'source': 'MOVIE', 'relationship': 'LANGUAGE', 'target': 'LANGUAGE'} #A Movie can be connected to many Languages
                            """
        self.instructions_for_query_gen_template =  """You are an experienced graph databases developer. 
                                                    This is the schema representation of a Neo4j database consisting of Movie Information Database.
                                                    \n\n\n """+self.graph_schema+""" \n\n\n Based on this schema, Generate a SINGLE CYPHER Query for Neo4j to 
                                                    retirive relevant information from data for the user's query strictly following sample srutcture\n
                                                    \n```cypher<CYPHER-QUERY>```"""
        
        self.instructions_for_response_gen_template = """ You are an Assistant and you are supposed to answer User's query precisely in natural language. 
                                                    Do not mention in your response anything about following/n/n Hint:"""
    
    def get_graph_query(self, user_query:str):
        history = [
            {"role": "system", "content": self.instructions_for_query_gen_template},
            {"role": "user", "content": user_query},]
        llm_output = self.client.chat.completions.create(model="model-identifier",
                                                         messages=history,
                                                         temperature=0.3,)
        return llm_output.choices[0].message.content

    def get_query_response(self, user_query:str, retrival_result):
        if retrival_result != None:
            instructions = self.instructions_for_response_gen_template+retrival_result
        else:
            instructions = self.instructions_for_response_gen_template
        history = [
            {"role": "system", "content": instructions},
            {"role": "user", "content": user_query},]
        llm_output = self.client.chat.completions.create(model="model-identifier",
                                                         messages=history,
                                                         temperature=0.6,)
        return llm_output.choices[0].message.content
        

    def process_result(self, llm_result:str):
        try:
            match = re.search(r'```cypher\s*(.*?)\s*```', llm_result, re.DOTALL)

            if not match:
                raise ValueError("No Cypher query found within triple backticks.")

            cypher_query = match.group(1).strip()
            return cypher_query
        except ValueError as e:
            return None