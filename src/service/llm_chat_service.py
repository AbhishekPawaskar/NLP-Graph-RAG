import json
import pydantic
from src.connectors.llm_connector import LLMConnection

class ChatService:
    def __init__(self):
        self.client = LLMConnection().client
        self.graph_schema =  """Nodes and their properties are the following:
                            {'label': 'MOVIE', 'properties': ['name', 'overview', 'cast']}
                            {'labels': 'GENRE','properties': ['genre']}
                            {'labels': 'LANGUAGE','properties': ['language']}


                            The relationships are the following:
                            {'source': 'MOVIE', 'relationship': 'GENRE', 'target': 'GENRE'} #A Movie can be connected to many Genres
                            {'source': 'MOVIE', 'relationship': 'LANGUAGE', 'target': 'LANGUAGE'} #A Movie can be connected to many Languages
                            """
        self.instructions_for_query_gen_template = """You are an experienced graph databases developer. This is the schema representation of a 
                                                    Neo4j database consisting of Movie Information Database.\n\n\n """+self.graph_schema+""" \n\n\n
                                                    Based on this schema, Generate CYPHER Query for Neo4j to retirive relevant information from data for 
                                                    the user's query strictly following srutcture\n \n{\n'query1':'<QUERY>,\n'query2':'<QUERY>'\n}\n"""
        self.instructions_for_response_gen_template = """ You are an Assistant and you are supposed to answer User's query precisely in natural language. 
                                                    Do not mention in your response anything about following/n/n Hint:"""
    
    def get_graph_query(self, user_query:str):
        history = [
            {"role": "system", "content": self.instructions_for_query_gen_template},
            {"role": "user", "content": user_query},]
        llm_output = self.client.chat.completions.create(model="model-identifier",
                                                         messages=history,
                                                         temperature=0.6,)
        return llm_output.choices[0].message.content

    def get_query_response(self, user_query:str, retrival_result:str):
        instructions = self.instructions_for_response_gen_template+retrival_result
        history = [
            {"role": "system", "content": instructions},
            {"role": "user", "content": user_query},]
        llm_output = self.client.chat.completions.create(model="model-identifier",
                                                         messages=history,
                                                         temperature=0.6,)
        return llm_output.choices[0].message.content
        

    def process_result(self, llm_result:str):
        try:
            processed_string_result = llm_result[llm_result.find('{'):llm_result.rfind('}') + 1]
            graph_data = json.loads(processed_string_result)
            return graph_data
        except pydantic.ValidationError as e:
            return None