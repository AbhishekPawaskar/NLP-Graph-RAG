from fastapi import FastAPI
from src.routes.route_controller import chat_routes

#only for debugging
# import debugpy
# debugpy.listen(("0.0.0.0", 5678))

app = FastAPI()
app.mount("/chat", chat_routes)