from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from app.routes import agents, conversations  # Add conversations import

load_dotenv()

app = FastAPI(title="ArkAgents API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "ArkAgents API is running! 🤖"}

@app.get("/health")
async def health():
    return {
        "status": "healthy", 
        "openai_key_set": bool(os.getenv("OPENAI_API_KEY"))
    }
@app.get("/test-conversations")
async def test():
    return {"message": "Conversations route works!"}
@app.get("/routes")
async def list_routes():
    routes = []
    for route in app.routes:
        routes.append({
            "path": route.path,
            "name": route.name,
        })
    return {"routes": routes}
# Include routers
app.include_router(agents.router)
app.include_router(conversations.router)  # Add this line

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)