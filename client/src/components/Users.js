import React, { useState, useEffect } from 'react';

function Users() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetch('http://localhost:4000/get_all_users')
      .then(response => response.json())
      .then(data => setUsers(data.users))
      .catch(error => console.error('Error fetching users:', error));
  }, []);

  return (
    <div>
      <h2>Users</h2>
      <ul>
        {users.map(user => (
          <li key={user.username}>{user.username} - {user.email}</li>
        ))}
      </ul>
    </div>
  );
}

export default Users;
