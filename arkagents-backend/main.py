from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from app.routes import agents

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

# Include agent routes
app.include_router(agents.router)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)