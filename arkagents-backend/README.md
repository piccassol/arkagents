# 🤖 ArkAgents - AI Agent Platform

> Create custom AI agents in seconds. Powered by Groq (Llama 3.3 70B).

## 🌟 Features

- **Custom AI Agents** - Create unlimited specialized agents
- **Real-time Chat** - Blazing fast responses (<2 seconds)
- **Conversation Memory** - Agents remember context
- **Multi-agent Support** - Switch between different agents
- **Beautiful UI** - Clean, modern chat interface
- **Free & Fast** - Powered by Groq's free tier

## 🚀 Quick Start

### Backend Setup
```bash
cd arkagents-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your GROQ_API_KEY

# Run server
python main.py
Frontend Setup
bashcd arkagents-frontend

# Install dependencies
npm install

# Start development server
npm start
🔑 Environment Variables
Create .env in arkagents-backend/:
GROQ_API_KEY=your_groq_api_key_here
PORT=8001
Get your free Groq API key: https://console.groq.com
📖 API Endpoints

POST /api/agents/create - Create new agent
GET /api/agents/list - List all agents
GET /api/agents/{id} - Get agent details
POST /api/agents/{id}/chat - Chat with agent
DELETE /api/agents/{id} - Delete agent

🛠️ Tech Stack
Backend:

FastAPI
Groq (Llama 3.3 70B)
Python 3.8+

Frontend:

React
Axios
Modern CSS

📊 Performance

Response time: <2 seconds
Free tier: 14,400 requests/day
Supports: 100+ concurrent users

🤝 Contributing
Part of Ark Technologies - Building AI-native business tools.
📝 License
MIT License - see LICENSE file
🔗 Links

Ark Technologies
ArkMail
Lead Gen Dashboard


Built with ❤️ by the Ark Technologies team

Save and close.

---

## Step 3: Create .env.example
```powershell
notepad .env.example
Paste this (WITHOUT your actual keys):
GROQ_API_KEY=your_groq_api_key_here
ARKMAIL_API_URL=https://arkmail-api.onrender.com
PORT=8001
Save and close.

Step 4: Initialize Git
powershell# Initialize git repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - ArkAgents AI platform"