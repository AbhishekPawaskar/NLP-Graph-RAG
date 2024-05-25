import os
import unicodedata
import pandas as pd
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

def add_genre_node(genre:str):
    records, summary, keys = driver.execute_query(
        "CREATE (g:GENRE {name: $genre})",
        genre=genre)

def add_language_node(language:str):
    records, summary, keys = driver.execute_query(
        "CREATE (l:LANGUAGE {name: $language})",
        language=language)

def add_movie_node(movie_name:str,overview:str,cast:str):
    records, summary, keys = driver.execute_query(
        "CREATE (m:MOVIE {name: $name, overview: $overview, cast: $cast})",
        name=movie_name,
        overview=overview,
        cast=cast)

def add_genre_edge(movie_name:str,genre:str):
    query = """MATCH (m:MOVIE {name: $name}), (g:GENRE {name: $genre}) CREATE (m)-[:GENRE]->(g)"""
    records, summary, keys = driver.execute_query(
        query,
        name=movie_name,
        genre=genre)

def add_lang_edge(movie_name:str,language:str):
    query = """MATCH (m:MOVIE {name: $name}), (l:LANGUAGE {name: $language}) CREATE (m)-[:LANGUAGE]->(l)"""
    records, summary, keys = driver.execute_query(
        query,
        name=movie_name,
        language=language)

if __name__ == "__main__":
    data = pd.read_csv("/app/assets/imdb_movies.csv")
    print("loaded data")
    data = data.dropna()

    lang_list = []
    lang_slice = data.iloc[:]["orig_lang"].to_list()
    for i in lang_slice:
        if type(i)==str:
            j = i.split(', ')
            for lang in j:
                if lang not in lang_list:
                    lang_list.append(lang)
                else:
                    continue

    genre_list = []
    genre_slice = data.iloc[:]["genre"].to_list()
    for i in genre_slice:
        if type(i)==str:
            j = unicodedata.normalize('NFKC', i).split(', ')
            for genre in j:
                if genre not in genre_list:
                    genre_list.append(genre)
                else:
                    continue

    year_list = []
    date_slice = data.iloc[:]["date_x"].to_list()
    for i in date_slice:
        if type(i)==str:
            j = i.split("/")[-1]
            if j not in year_list:
                year_list.append(j)
            else:
                continue

    driver = Neo4jConnection.get_driver()


    for i in genre_list:
        add_genre_node(genre=i)
    print("genre uploaded")

    for i in lang_list:
        add_language_node(language=i)
    print("language uploaded")

    for row in data.iterrows():
        row_data = row[1].to_dict()
        g_list = unicodedata.normalize('NFKC', row_data['genre']).split(', ')
        l_list = row_data['orig_lang'].split(', ')
        add_movie_node(movie_name=row_data["orig_title"], 
                    overview=row_data["overview"], 
                    cast=row_data["crew"])
        if (g_list != None) or (g_list!=[]):
            for g in g_list:
                add_genre_edge(movie_name=row_data["orig_title"],genre=g)
        if (l_list != None) or (l_list!=[]):
            for l in l_list:
                add_lang_edge(movie_name=row_data["orig_title"],language=l)
    print("movie uploaded")

    print("##### UPLOAD COMPLETE #####")
    
    
