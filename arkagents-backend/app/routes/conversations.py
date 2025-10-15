from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, and_
from app.database import get_db
from app.models import AgentConversation, Agent
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from groq import Groq
import os

router = APIRouter(prefix="/api/conversations", tags=["conversations"])

class SendMessageRequest(BaseModel):
    message: str

@router.get("/list")
async def list_conversations(
    agent_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    List conversation 'sessions' grouped by agent and time.
    Since we don't have a conversations table, we'll group messages by agent_id
    and create pseudo-conversations based on time gaps.
    """
    query = select(
        AgentConversation.agent_id,
        func.min(AgentConversation.created_at).label('first_message'),
        func.max(AgentConversation.created_at).label('last_message'),
        func.count(AgentConversation.id).label('message_count')
    ).group_by(AgentConversation.agent_id)
    
    if agent_id:
        query = query.where(AgentConversation.agent_id == agent_id)
    
    query = query.order_by(desc('last_message'))
    
    result = await db.execute(query)
    conversations = result.all()
    
    return {
        "conversations": [
            {
                "id": f"agent_{conv.agent_id}",  # Pseudo ID
                "agent_id": conv.agent_id,
                "title": f"Chat - {conv.first_message.strftime('%b %d, %I:%M %p')}",
                "message_count": conv.message_count,
                "created_at": conv.first_message.isoformat(),
                "updated_at": conv.last_message.isoformat()
            }
            for conv in conversations
        ]
    }

@router.get("/agent/{agent_id}")
async def get_agent_conversation(
    agent_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all messages for an agent (this is essentially the conversation)"""
    query = select(AgentConversation).where(
        AgentConversation.agent_id == agent_id
    ).order_by(AgentConversation.created_at)
    
    result = await db.execute(query)
    messages = result.scalars().all()
    
    return {
        "id": f"agent_{agent_id}",
        "agent_id": agent_id,
        "title": f"Chat with Agent {agent_id}",
        "messages": [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.message,
                "created_at": msg.created_at.isoformat()
            }
            for msg in messages
        ]
    }

@router.post("/agent/{agent_id}/message")
async def send_message(
    agent_id: int,
    request: SendMessageRequest,
    db: AsyncSession = Depends(get_db)
):
    """Send a message to an agent"""
    
    # Get agent details
    agent_query = select(Agent).where(Agent.id == agent_id)
    agent_result = await db.execute(agent_query)
    agent = agent_result.scalar_one_or_none()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Save user message
    user_message = AgentConversation(
        agent_id=agent_id,
        user_id="default_user",
        role="user",
        message=request.message
    )
    db.add(user_message)
    await db.flush()
    
    # Get conversation history
    history_query = select(AgentConversation).where(
        AgentConversation.agent_id == agent_id
    ).order_by(AgentConversation.created_at)
    
    history_result = await db.execute(history_query)
    history = history_result.scalars().all()
    
    # Build messages for Groq
    messages_for_groq = []
    
    # Add system prompt if exists
    if agent.system_prompt:
        messages_for_groq.append({
            "role": "system",
            "content": agent.system_prompt
        })
    
    # Add conversation history
    for msg in history:
        messages_for_groq.append({
            "role": msg.role,
            "content": msg.message
        })
    
    # Add new user message
    messages_for_groq.append({
        "role": "user",
        "content": request.message
    })
    
    # Get AI response
    try:
        groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages_for_groq,
            temperature=0.7,
            max_tokens=2000
        )
        
        assistant_response = completion.choices[0].message.content
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error calling Groq: {str(e)}")
    
    # Save assistant response
    assistant_message = AgentConversation(
        agent_id=agent_id,
        user_id="default_user",
        role="assistant",
        message=assistant_response
    )
    db.add(assistant_message)
    
    await db.commit()
    
    return {
        "message": assistant_response,
        "message_id": assistant_message.id
    }

@router.delete("/agent/{agent_id}")
async def delete_agent_conversation(
    agent_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete all messages for an agent"""
    query = select(AgentConversation).where(
        AgentConversation.agent_id == agent_id
    )
    
    result = await db.execute(query)
    messages = result.scalars().all()
    
    for msg in messages:
        await db.delete(msg)
    
    await db.commit()
    
    return {"success": True, "message": f"Deleted {len(messages)} messages"}