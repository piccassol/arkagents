import React, { useState, useEffect } from 'react';
import AgentTemplates from './components/AgentTemplates';
import AnalyticsDashboard from './components/AnalyticsDashboard';
import './App.css';

const API_URL = 'https://api.arktechnologies.ai';

function App() {
  const [agents, setAgents] = useState([]);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [showCreateAgent, setShowCreateAgent] = useState(false);
  const [showTemplates, setShowTemplates] = useState(false);
  const [showAnalytics, setShowAnalytics] = useState(false);
  const [newAgentName, setNewAgentName] = useState('');
  const [newAgentDesc, setNewAgentDesc] = useState('');
  const [newAgentPrompt, setNewAgentPrompt] = useState('');

  // Load agents on mount
  useEffect(() => {
    loadAgents();
  }, []);

  // Load conversation when agent is selected
  useEffect(() => {
    if (selectedAgent) {
      loadConversation(selectedAgent.id);
    }
  }, [selectedAgent]);

  const loadAgents = async () => {
    try {
      const response = await fetch(`${API_URL}/api/agents/list`);
      const data = await response.json();
      setAgents(data.agents);
    } catch (error) {
      console.error('Error loading agents:', error);
    }
  };

  const loadConversation = async (agentId) => {
    try {
      const response = await fetch(`${API_URL}/api/agents/${agentId}/conversation`);
      const data = await response.json();
      
      // The data.conversation is already in the right format
      setMessages(data.conversation || []);
    } catch (error) {
      console.error('Error loading conversation:', error);
      setMessages([]);
    }
  };

  const createAgent = async () => {
    try {
      const response = await fetch(`${API_URL}/api/agents/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: newAgentName,
          description: newAgentDesc,
          system_prompt: newAgentPrompt || undefined
        })
      });
      const agent = await response.json();
      setAgents([...agents, agent]);
      setShowCreateAgent(false);
      setNewAgentName('');
      setNewAgentDesc('');
      setNewAgentPrompt('');
      setSelectedAgent(agent);
      setMessages([]);
    } catch (error) {
      console.error('Error creating agent:', error);
    }
  };

  const createAgentFromTemplate = async (template) => {
    try {
      const response = await fetch(`${API_URL}/api/agents/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: template.name,
          description: template.description,
          system_prompt: template.systemPrompt
        })
      });
      const agent = await response.json();
      setAgents([...agents, agent]);
      setShowTemplates(false);
      setSelectedAgent(agent);
      setMessages([]);
    } catch (error) {
      console.error('Error creating agent from template:', error);
      alert('Failed to create agent. Please try again.');
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || !selectedAgent) return;

    const userMessage = { role: 'user', message: inputMessage };
    setMessages([...messages, userMessage]);
    setInputMessage('');
    setLoading(true);

    try {
      const response = await fetch(
        `${API_URL}/api/agents/${selectedAgent.id}/chat`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: inputMessage })
        }
      );
      const data = await response.json();

      setMessages(prev => [...prev, {
        role: 'assistant',
        message: data.message
      }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        message: 'Error: Could not get response from agent'
      }]);
    } finally {
      setLoading(false);
    }
  };

  const clearConversation = async () => {
    if (!selectedAgent) return;
    if (!window.confirm('Clear all messages with this agent?')) return;

    // For in-memory storage, just clear locally
    setMessages([]);
  };

  // If showing templates, render that instead
  if (showTemplates) {
    return (
      <AgentTemplates
        onUseTemplate={createAgentFromTemplate}
        onClose={() => setShowTemplates(false)}
      />
    );
  }

  // If showing analytics, render that instead
  if (showAnalytics) {
    return (
      <AnalyticsDashboard
        onClose={() => setShowAnalytics(false)}
      />
    );
  }

  return (
    <div className="App">
      {/* Sidebar */}
      <div className="sidebar">
        <h2>🤖 ArkAgents</h2>

        <button
          className="create-btn"
          onClick={() => setShowCreateAgent(true)}
        >
          + New Agent
        </button>

        <button
          className="templates-btn"
          onClick={() => setShowTemplates(true)}
          style={{
            marginTop: '10px',
            width: '100%',
            padding: '12px',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontWeight: '600'
          }}
        >
          📚 Browse Templates
        </button>

        <button
          onClick={() => setShowAnalytics(true)}
          style={{
            marginTop: '10px',
            width: '100%',
            padding: '12px',
            background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontWeight: '600'
          }}
        >
          📊 Analytics
        </button>

        <div className="agents-list">
          {agents.map(agent => (
            <div
              key={agent.id}
              className={`agent-item ${selectedAgent?.id === agent.id ? 'active' : ''}`}
              onClick={() => {
                setSelectedAgent(agent);
              }}
            >
              <div className="agent-name">{agent.name}</div>
              <div className="agent-desc">{agent.description}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="main-content">
        {selectedAgent ? (
          <>
            <div className="chat-header">
              <div>
                <h3>{selectedAgent.name}</h3>
                <p>{selectedAgent.description}</p>
              </div>
              {messages.length > 0 && (
                <button
                  onClick={clearConversation}
                  style={{
                    padding: '8px 16px',
                    background: '#ef4444',
                    color: 'white',
                    border: 'none',
                    borderRadius: '6px',
                    cursor: 'pointer',
                    fontSize: '14px'
                  }}
                >
                  🗑️ Clear Chat
                </button>
              )}
            </div>

            <div className="messages">
              {messages.map((msg, idx) => (
                <div key={idx} className={`message ${msg.role}`}>
                  <div className="message-content">
                    {msg.message}
                  </div>
                </div>
              ))}
              {loading && (
                <div className="message assistant">
                  <div className="message-content typing">
                    Agent is thinking...
                  </div>
                </div>
              )}
            </div>

            <div className="input-area">
              <input
                id="chat-input"
                name="message"
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                placeholder="Type your message..."
                disabled={loading}
              />
              <button onClick={sendMessage} disabled={loading}>
                Send
              </button>
            </div>
          </>
        ) : (
          <div className="empty-state">
            <h2>Welcome to ArkAgents</h2>
            <p>Select an agent or create a new one to get started</p>
            <button
              onClick={() => setShowTemplates(true)}
              style={{
                marginTop: '20px',
                padding: '12px 24px',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                fontSize: '16px',
                fontWeight: '600'
              }}
            >
              Browse Agent Templates
            </button>
          </div>
        )}
      </div>

      {/* Create Agent Modal */}
      {showCreateAgent && (
        <div className="modal-overlay" onClick={() => setShowCreateAgent(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <h3>Create New Agent</h3>
            <input
              id="agent-name"
              name="agent-name"
              type="text"
              placeholder="Agent Name (e.g., Sales Assistant)"
              value={newAgentName}
              onChange={(e) => setNewAgentName(e.target.value)}
            />
            <textarea
              id="agent-description"
              name="agent-description"
              placeholder="Description (e.g., helps with sales outreach)"
              value={newAgentDesc}
              onChange={(e) => setNewAgentDesc(e.target.value)}
              rows={3}
            />
            <textarea
              id="agent-prompt"
              name="agent-prompt"
              placeholder="System Prompt (optional - defines agent behavior)"
              value={newAgentPrompt}
              onChange={(e) => setNewAgentPrompt(e.target.value)}
              rows={4}
            />
            <div className="modal-buttons">
              <button onClick={() => setShowCreateAgent(false)}>Cancel</button>
              <button onClick={createAgent} className="primary">Create</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;