from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import os

router = APIRouter(prefix="/api/agents", tags=["agents"])

# In-memory storage (we'll add database later)
agents_db = {}
conversations_db = {}
agent_id_counter = 1

# ============= REQUEST/RESPONSE MODELS =============

class CreateAgentRequest(BaseModel):
    name: str
    description: str
    system_prompt: Optional[str] = None

class ChatRequest(BaseModel):
    message: str

class AgentResponse(BaseModel):
    id: int
    name: str
    description: str
    system_prompt: str

# ============= ENDPOINTS =============

@router.post("/create", response_model=AgentResponse)
async def create_agent(request: CreateAgentRequest):
    """Create a new AI agent"""
    global agent_id_counter
    
    # Generate default prompt if none provided
    if not request.system_prompt:
        request.system_prompt = f"""You are {request.name}, an AI assistant that helps with {request.description}.

You are helpful, accurate, and efficient. Always provide clear and actionable responses.
If you're not sure about something, ask for clarification."""
    
    agent = {
        "id": agent_id_counter,
        "name": request.name,
        "description": request.description,
        "system_prompt": request.system_prompt,
        "user_id": "demo_user",  # We'll add auth later
        "created_at": "2025-10-11"
    }
    
    agents_db[agent_id_counter] = agent
    conversations_db[agent_id_counter] = []
    agent_id_counter += 1
    
    return agent


@router.get("/list")
async def list_agents():
    """Get all agents"""
    return {"agents": list(agents_db.values())}


@router.get("/{agent_id}")
async def get_agent(agent_id: int):
    """Get a specific agent"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agents_db[agent_id]


@router.post("/{agent_id}/chat")
async def chat_with_agent(agent_id: int, request: ChatRequest):
    """Chat with an AI agent"""
    
    print(f"🔍 CHAT REQUEST: agent_id={agent_id}, message={request.message}")
    
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agent = agents_db[agent_id]
    conversation_history = conversations_db.get(agent_id, [])
    
    print(f"🔍 Found agent: {agent['name']}")
    
    # Save user message
    conversation_history.append({
        "role": "user",
        "message": request.message
    })
    
    print(f"🔍 About to import call_openai...")
    
    # Call OpenAI
    from app.services.ai_service import call_openai
    
    print(f"🔍 Import successful, calling AI...")
    
    try:
        response = await call_openai(
            system_prompt=agent["system_prompt"],
            user_message=request.message,
            conversation_history=conversation_history
        )
        
        print(f"🔍 Got AI response: {response[:50]}...")
        
        # Save assistant response
        conversation_history.append({
            "role": "assistant",
            "message": response
        })
        
        conversations_db[agent_id] = conversation_history
        
        return {
            "message": response,
            "agent_name": agent["name"]
        }
        
    except Exception as e:
        print(f"❌ ERROR in chat: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error calling OpenAI: {str(e)}")


@router.delete("/{agent_id}")
async def delete_agent(agent_id: int):
    """Delete an agent"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    del agents_db[agent_id]
    if agent_id in conversations_db:
        del conversations_db[agent_id]
    
    return {"message": "Agent deleted successfully"}


@router.get("/{agent_id}/conversation")
async def get_conversation(agent_id: int):
    """Get conversation history for an agent"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return {
        "agent_id": agent_id,
        "conversation": conversations_db.get(agent_id, [])
    }