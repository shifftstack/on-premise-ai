import React, { useState } from 'react';
import { chatQuery } from '../../utils/api';
import { getToken } from '../../utils/auth';
import MessageBubble from './MessageBubble';

function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    setMessages([...messages, { text: input, isUser: true }]);
    setLoading(true);
    setError('');
    try {
      const res = await chatQuery(input, getToken());
      setMessages(msgs => [...msgs, { text: res.answer, isUser: false, sources: res.sources }]);
    } catch (err) {
      setMessages(msgs => [...msgs, { text: 'Error: Could not get answer.', isUser: false }]);
      setError('Chat failed: ' + (err.message || 'Unknown error'));
    }
    setInput('');
    setLoading(false);
  };

  return (
    <div>
      <h2>Chat</h2>
      <div style={{ minHeight: 200, border: '1px solid #ccc', padding: 8, marginBottom: 8 }}>
        {messages.map((msg, i) => (
          <div key={i}>
            <MessageBubble message={msg.text} isUser={msg.isUser} />
            {msg.sources && msg.sources.length > 0 && (
              <div style={{ fontSize: '0.8em', color: '#888' }}>
                Sources: {msg.sources.join(', ')}
              </div>
            )}
          </div>
        ))}
        {loading && <div>Loading...</div>}
      </div>
      <form onSubmit={handleSend} style={{ display: 'flex' }}>
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          disabled={loading}
          style={{ flex: 1 }}
        />
        <button type="submit" disabled={loading || !input.trim()}>Send</button>
      </form>
      {error && <div style={{ color: 'red' }}>{error}</div>}
    </div>
  );
}

export default ChatWindow; 