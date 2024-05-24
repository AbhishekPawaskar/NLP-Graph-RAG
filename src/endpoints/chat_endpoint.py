from src.datamodels.models import ConversationRequest, ConversationResponse
from src.service.graph_db_service import execute_graph_query
from src.service.llm_chat_service import ChatService

llm_chat_service = ChatService()

def conversation_endpoint(request_body: ConversationRequest):
    llm_cypher_query_response = llm_chat_service.get_graph_query(user_query=request_body.query)
    cypher_query = llm_chat_service.process_result(llm_result=llm_cypher_query_response)
    retrival_result = execute_graph_query(cypher_query)
    user_query_response = llm_chat_service.get_query_response(user_query=request_body.query,
                                                              retrival_result=retrival_result)
    return ConversationResponse(userId=request_body.userId,queryResponse=user_query_response)
