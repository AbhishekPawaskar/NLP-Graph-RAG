from fastapi import APIRouter
from src.endpoints.chat_endpoint import conversation_endpoint
from src.utility.custom_seriliaze import ORJSONResponse

chat_routes = APIRouter()
chat_routes.add_api_route("/converse", conversation_endpoint, methods=["POST"], response_class=ORJSONResponse)