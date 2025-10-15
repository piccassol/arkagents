from sqlalchemy import Column, String, Text, DateTime, Integer, JSON
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base
from datetime import datetime

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    system_prompt = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class AgentConversation(Base):
    """This table stores individual messages, not conversations"""
    __tablename__ = "agent_conversations"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    agent_id = Column(Integer, nullable=False)
    user_id = Column(String(255), nullable=False, default="default_user")
    role = Column(String(50), nullable=False)  # 'user' or 'assistant'
    message = Column(Text, nullable=False)
    tool_calls = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)