import React, { useState, useEffect } from 'react';
import { getToken } from '../../utils/auth';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

async function listUsers(token) {
  const res = await fetch(`${API_URL}/admin/users`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('List users failed');
  return res.json();
}

async function deleteUser(email, token) {
  const res = await fetch(`${API_URL}/admin/users/${encodeURIComponent(email)}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('Delete user failed');
  return res.json();
}

function UserManagement() {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const fetchUsers = async () => {
    try {
      const users = await listUsers(getToken());
      setUsers(users);
    } catch (err) {
      setError('Could not fetch users');
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleDelete = async (email) => {
    setError('');
    setSuccess('');
    try {
      await deleteUser(email, getToken());
      setSuccess('User deleted');
      fetchUsers();
    } catch (err) {
      setError('Delete failed');
    }
  };

  return (
    <div>
      <h2>User Management (Admin Only)</h2>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {success && <div style={{ color: 'green' }}>{success}</div>}
      <ul>
        {users.map((user, i) => (
          <li key={i}>
            {user.email} {user.is_admin && '(admin)'}
            <button onClick={() => handleDelete(user.email)} style={{ marginLeft: 8 }}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default UserManagement; 