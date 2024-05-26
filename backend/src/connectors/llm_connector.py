import os
from openai import OpenAI

#Singleton class implementation
class LLMConnection:
    _instance = None
    
    def __init__(self):
        self.client = establish_remote_connection()
        
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMConnection, cls).__new__(cls) 
            cls._instance.__init__()
        else:
            if cls._instance.client is None or cls._instance.client.is_closed(): 
                cls._instance.client = establish_remote_connection()
                
        return cls._instance
    

def establish_remote_connection():
    client = OpenAI(base_url=os.environ.get('LLM_BASE_URL'), api_key=os.environ.get('LLM_KEY'))
    return client