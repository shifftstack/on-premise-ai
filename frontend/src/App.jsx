import React, { useState } from 'react';
import LoginForm from './components/Auth/LoginForm';
import RegisterForm from './components/Auth/RegisterForm';
import ChatWindow from './components/Chat/ChatWindow';
import DocumentManagement from './components/Admin/DocumentManagement';
import UserManagement from './components/Admin/UserManagement';
import { getToken, clearToken } from './utils/auth';

function parseJwt(token) {
  if (!token) return {};
  try {
    return JSON.parse(atob(token.split('.')[1]));
  } catch {
    return {};
  }
}

function App() {
  const [loggedIn, setLoggedIn] = useState(!!getToken());
  const [showRegister, setShowRegister] = useState(false);
  const token = getToken();
  const user = parseJwt(token);

  const handleLogout = () => {
    clearToken();
    setLoggedIn(false);
  };

  if (!loggedIn) {
    return (
      <div>
        {showRegister ? (
          <>
            <RegisterForm onRegister={() => setLoggedIn(true)} />
            <button onClick={() => setShowRegister(false)}>Back to Login</button>
          </>
        ) : (
          <>
            <LoginForm onLogin={() => setLoggedIn(true)} />
            <button onClick={() => setShowRegister(true)}>Register</button>
          </>
        )}
      </div>
    );
  }

  return (
    <div>
      <button onClick={handleLogout}>Logout</button>
      <h1>OnPremiseAI</h1>
      <div style={{ marginBottom: 16 }}>
        Logged in as: {user.sub} {user.is_admin && '(admin)'}
      </div>
      <ChatWindow />
      <DocumentManagement />
      {user.is_admin && <UserManagement />}
    </div>
  );
}

export default App; 