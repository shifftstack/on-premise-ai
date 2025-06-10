import React from 'react';

function MessageBubble({ message, isUser }) {
  return (
    <div style={{
      textAlign: isUser ? 'right' : 'left',
      margin: '8px 0',
    }}>
      <span style={{
        display: 'inline-block',
        background: isUser ? '#cce5ff' : '#e2e2e2',
        padding: '8px 12px',
        borderRadius: '16px',
        maxWidth: '70%',
      }}>{message}</span>
    </div>
  );
}

export default MessageBubble; 