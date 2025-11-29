// App.js
import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [tasks, setTasks] = useState([]);
  const [conversations, setConversations] = useState({});
  const [riskyResponses, setRiskyResponses] = useState([]);
  const [aiIncidents, setAiIncidents] = useState([]);
  const [selectedTask, setSelectedTask] = useState(null);
  const [userMessage, setUserMessage] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch initial data
    fetchTasks();
    fetchRiskyResponses();
    fetchAiIncidents();
  }, []);

  const fetchTasks = async () => {
    try {
      const response = await fetch('/api/tasks');
      const data = await response.json();
      setTasks(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching tasks:', error);
      setLoading(false);
    }
  };

  const fetchRiskyResponses = async () => {
    try {
      const response = await fetch('/api/risky-responses');
      const data = await response.json();
      setRiskyResponses(data);
    } catch (error) {
      console.error('Error fetching risky responses:', error);
    }
  };

  const fetchAiIncidents = async () => {
    try {
      const response = await fetch('/api/ai-incidents');
      const data = await response.json();
      setAiIncidents(data);
    } catch (error) {
      console.error('Error fetching AI incidents:', error);
    }
  };

  const fetchConversation = async (taskId) => {
    try {
      const response = await fetch(`/api/conversations/${taskId}`);
      const data = await response.json();
      setConversations(prev => ({
        ...prev,
        [taskId]: data
      }));
      setSelectedTask(taskId);
    } catch (error) {
      console.error(`Error fetching conversation for task ${taskId}:`, error);
    }
  };

  const handleTaskClick = (taskId) => {
    if (!conversations[taskId]) {
      fetchConversation(taskId);
    } else {
      setSelectedTask(taskId);
    }
  };

  const handleMessageSubmit = async (e) => {
    e.preventDefault();
    if (!userMessage.trim() || !selectedTask) return;

    // Add user message to the UI immediately
    const tempMessage = { role: 'human', content: userMessage };
    setConversations(prev => ({
      ...prev,
      [selectedTask]: [...(prev[selectedTask] || []), tempMessage]
    }));
    setUserMessage('');

    // Send to API
    try {
      const response = await fetch(`/api/conversations/${selectedTask}/messages`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
      });
      
      const data = await response.json();
      
      // Update with AI response
      setConversations(prev => ({
        ...prev,
        [selectedTask]: [...(prev[selectedTask] || []), { role: 'ai', content: data.response }]
      }));
      
      // Check if response was flagged as risky
      if (data.is_risky) {
        setRiskyResponses(prev => [...prev, {
          task_id: selectedTask,
          message: userMessage,
          response: data.response,
          reason: data.risk_reason
        }]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div className="app-container">
      <div className="panel human-agent-panel">
        <h2>Human-Agent Interaction</h2>
        <div className="interaction-container">
          <div className="task-list">
            {loading ? (
              <p>Loading tasks...</p>
            ) : (
              tasks.map(task => (
                <div 
                  key={task.id} 
                  className={`task-item ${selectedTask === task.id ? 'selected' : ''}`}
                  onClick={() => handleTaskClick(task.id)}
                >
                  Task {task.id}
                </div>
              ))
            )}
          </div>
          
          <div className="conversation-view">
            {selectedTask && conversations[selectedTask] ? (
              <>
                <div className="messages-container">
                  {conversations[selectedTask].map((message, index) => (
                    <div key={index} className={`message ${message.role}`}>
                      <div className="message-icon">
                        {message.role === 'ai' ? '🤖' : '👤'}
                      </div>
                      <div className="message-content">{message.content}</div>
                    </div>
                  ))}
                </div>
                <form className="message-input-form" onSubmit={handleMessageSubmit}>
                  <input
                    type="text"
                    value={userMessage}
                    onChange={(e) => setUserMessage(e.target.value)}
                    placeholder="Type your message..."
                  />
                  <button type="submit">Send</button>
                </form>
              </>
            ) : (
              <div className="empty-state">
                {selectedTask ? 'Loading conversation...' : 'Select a task to view conversation'}
              </div>
            )}
          </div>
        </div>
      </div>
      
      <div className="panel value-audit-panel">
        <h2>Value Auditing Panel</h2>
        
        <div className="audit-section">
          <h3>Risky Responses & Values</h3>
          <div className="audit-content">
            {riskyResponses.length > 0 ? (
              riskyResponses.map((item, index) => (
                <div key={index} className="audit-item">
                  <h4>Task {item.task_id} - Flagged Response</h4>
                  <div className="audit-details">
                    <p><strong>User:</strong> {item.message}</p>
                    <p><strong>AI:</strong> {item.response}</p>
                    <p><strong>Reason:</strong> {item.reason}</p>
                  </div>
                </div>
              ))
            ) : (
              <p>No risky responses detected</p>
            )}
          </div>
        </div>
        
        <div className="audit-section">
          <h3>Real AI Incidents</h3>
          <div className="audit-content">
            {aiIncidents.length > 0 ? (
              aiIncidents.map((incident, index) => (
                <div key={index} className="audit-item">
                  <h4>{incident.title}</h4>
                  <p>{incident.description}</p>
                  <p className="incident-date">{incident.date}</p>
                </div>
              ))
            ) : (
              <p>No incidents to display</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;