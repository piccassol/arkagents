from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    system_prompt = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AgentTool(Base):
    __tablename__ = "agent_tools"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, nullable=False, index=True)
    tool_name = Column(String(255), nullable=False)
    tool_description = Column(Text, nullable=False)
    n8n_webhook_url = Column(Text)
    parameters = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class AgentConversation(Base):
    __tablename__ = "agent_conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, nullable=False, index=True)
    user_id = Column(String(255), nullable=False, index=True)
    role = Column(String(50), nullable=False)  # 'user' or 'assistant'
    message = Column(Text, nullable=False)
    tool_calls = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)