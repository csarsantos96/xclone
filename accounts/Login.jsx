import React, { useState } from 'react';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Exemplo de requisição usando fetch:
      const response = await fetch('http://127.0.0.1:8000/api/accounts/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username,
          password: password,
        }),
      });

      if (response.ok) {
        // Login bem-sucedido
        const data = await response.json();

        // Se for Token Authentication, possivelmente data terá um token
        // Exemplo:
        // localStorage.setItem('token', data.token);

        alert('Login realizado com sucesso!');
        // Redirecionar ou alterar estado de logado
      } else {
        // Se a resposta não for 2xx, tratamos como erro
        const errData = await response.json();
        setErrorMsg(errData.detail || 'Credenciais inválidas');
      }
    } catch (error) {
      console.error('Erro ao logar:', error);
      setErrorMsg('Ocorreu um erro no servidor. Tente novamente mais tarde.');
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '0 auto', marginTop: '2rem' }}>
      <h2>Login</h2>
      {errorMsg && <p style={{ color: 'red' }}>{errorMsg}</p>}
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '1rem' }}>
          <label>Username:</label>
          <input
            type="text"
            name="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', marginTop: '4px' }}
          />
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label>Password:</label>
          <input
            type="password"
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', marginTop: '4px' }}
          />
        </div>
        <button type="submit" style={{ padding: '8px 16px' }}>
          Entrar
        </button>
      </form>
    </div>
  );
}

export default Login;
