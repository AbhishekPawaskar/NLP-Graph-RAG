
# NLP-Graph-RAG

This repository bears the source code for setup, deployment of LLM based Retrival Agumented Generation System.

## Content:

1. Overview and Tech Stack
2. API Endpoints
3. Setup & Usage

## 1. Overview and Tech Stack:


Following is the Diagram representing the system Overview.

![Picture1](https://github.com/AbhishekPawaskar/NLP-Graph-RAG/assets/46342691/730e1942-6e12-490b-a269-08c1e38d275f)

The Tech Stack are ars follows:
1. Frontend - Streamlit
2. Backend - FastAPI
3. LLMs - Llama2 (using LM Studio)
4. Graph Data Base - Neo4j (Community Edition)
5. Data Used - Movie Data Set (Available in `/setup/assets/imdb_movies.csv`)



## 2. API Endpoints :

 (REFER `/backend/src/datamodels/models.py` FOR DETAILED INFO ON REQUEST BODY)

a. `/chat/converse` : This endpoint is responsible to generate responses for user queries based on retrived Data. 
 
## 3. Setup & Usage:

### a. Setting up of Llama 2:

a. Install LM Studio

b. Navigate to search and look for `TheBloke/Llama-2-7B-Chat-GGUF/llama-2-7b-chat.Q3_K_S.gguf`. Download this model.

c. Navigate to local Server and load the model.

d. The LLM is now available for requests.

![image](https://github.com/AbhishekPawaskar/NLP-Graph-RAG/assets/46342691/ada0b816-e6b3-4956-915e-fb29a7328e09)



### b. Build & Run the Microservice:

```bash
# Turn on Docker in the system. Navigate to the cloned version of this repository and run the following commands

$  docker-compose build

$  docker-compose up 

```

### c. Graph DB Credentials & Upload the Data:

 1. Navigate to the link `http://localhost:7474/` and enter both the `username` and `password` as `neo4j` for `bolt` driver. 

 2. Change the `password`. For example here as `password` itself. (Should be same in `docker-compose.yml` file environment variables).

 3. The Graph Database dashboard will be unlocked.

 4. Navigate to Docker Desktop -> containers> restart the `setup` container. 

 5. Post exit of `setup` container with exit code '0', the Data is uploaded to Graph DB and is available to use.

 6. Navigate to `http://localhost:8501` on browser for the frontend interface to post queries and receive results. 

 (NOTE: the time taken to generate might be more than expected due to resource sharing and consumption)
