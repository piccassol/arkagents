import React, { useState, useEffect } from 'react';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

function App() {
  const [agents, setAgents] = useState([]);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [showCreateAgent, setShowCreateAgent] = useState(false);
  const [newAgentName, setNewAgentName] = useState('');
  const [newAgentDesc, setNewAgentDesc] = useState('');

  // Load agents on mount
  useEffect(() => {
    loadAgents();
  }, []);

  const loadAgents = async () => {
    try {
      const response = await fetch(`${API_URL}/api/agents/list`);
      const data = await response.json();
      setAgents(data.agents);
    } catch (error) {
      console.error('Error loading agents:', error);
    }
  };

  const createAgent = async () => {
    try {
      const response = await fetch(`${API_URL}/api/agents/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: newAgentName,
          description: newAgentDesc
        })
      });
      const agent = await response.json();
      setAgents([...agents, agent]);
      setShowCreateAgent(false);
      setNewAgentName('');
      setNewAgentDesc('');
      setSelectedAgent(agent);
      setMessages([]);
    } catch (error) {
      console.error('Error creating agent:', error);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || !selectedAgent) return;

    const userMessage = { role: 'user', message: inputMessage };
    setMessages([...messages, userMessage]);
    setInputMessage('');
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/agents/${selectedAgent.id}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: inputMessage })
      });
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

        <div className="agents-list">
          {agents.map(agent => (
            <div
              key={agent.id}
              className={`agent-item ${selectedAgent?.id === agent.id ? 'active' : ''}`}
              onClick={() => {
                setSelectedAgent(agent);
                setMessages([]);
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
              <h3>{selectedAgent.name}</h3>
              <p>{selectedAgent.description}</p>
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
          </div>
        )}
      </div>

      {/* Create Agent Modal */}
      {showCreateAgent && (
        <div className="modal-overlay" onClick={() => setShowCreateAgent(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <h3>Create New Agent</h3>
            <input
              type="text"
              placeholder="Agent Name (e.g., Sales Assistant)"
              value={newAgentName}
              onChange={(e) => setNewAgentName(e.target.value)}
            />
            <textarea
              placeholder="Description (e.g., helps with sales outreach)"
              value={newAgentDesc}
              onChange={(e) => setNewAgentDesc(e.target.value)}
              rows={3}
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