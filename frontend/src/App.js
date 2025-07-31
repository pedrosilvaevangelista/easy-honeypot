import React, { useState, useEffect, useCallback } from 'react';
import './styles.css';

function App() {
  const [attempts, setAttempts] = useState([]);
  const [stats, setStats] = useState({ total_attempts: 0, unique_ips: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(null);
  const [isUpdating, setIsUpdating] = useState(false); // Prevenir múltiplas chamadas

  // Detectar o IP correto baseado na URL atual
  const getCurrentHostIP = () => {
    return window.location.hostname;
  };

  // Tentar múltiplas URLs do backend
  const API_URLS = [
    process.env.REACT_APP_API_URL?.replace('${HOST_IP}', getCurrentHostIP()) || `http://${getCurrentHostIP()}:8000`,
    `http://${getCurrentHostIP()}:8000`,
    'http://localhost:8000',
    'http://127.0.0.1:8000'
  ];
  
  const [currentApiUrl, setCurrentApiUrl] = useState(API_URLS[0]);
  
  console.log('Hostname detectado:', getCurrentHostIP());
  console.log('URLs tentativas:', API_URLS);
  console.log('Tentando conectar com:', currentApiUrl);

  const fetchAttempts = useCallback(async () => {
    for (const apiUrl of API_URLS) {
      try {
        console.log(`Tentando conectar: ${apiUrl}/attempts/`);
        const response = await fetch(`${apiUrl}/attempts/`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setAttempts(data);
        setError(null);
        setLastUpdate(new Date());
        
        // Se chegou até aqui, esta URL funciona
        if (currentApiUrl !== apiUrl) {
          console.log(`Conectado com sucesso usando: ${apiUrl}`);
          setCurrentApiUrl(apiUrl);
        }
        return; // Sair do loop se teve sucesso
      } catch (err) {
        console.error(`Erro com ${apiUrl}:`, err);
        continue; // Tentar próxima URL
      }
    }
    
    // Se chegou aqui, nenhuma URL funcionou
    setError('Não foi possível conectar com nenhuma URL do backend');
  }, [API_URLS, currentApiUrl]);

  const fetchStats = useCallback(async () => {
    try {
      const response = await fetch(`${currentApiUrl}/stats/`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setStats(data);
    } catch (err) {
      console.error("Error fetching stats:", err);
    }
  }, [currentApiUrl]);

  const fetchData = useCallback(async () => {
    if (isUpdating) {
      console.log('Update já em andamento, pulando...');
      return;
    }
    
    setIsUpdating(true);
    try {
      await Promise.all([fetchAttempts(), fetchStats()]);
      setLoading(false);
    } catch (error) {
      console.error('Erro ao buscar dados:', error);
    } finally {
      setIsUpdating(false);
    }
  }, [fetchAttempts, fetchStats, isUpdating]);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000); // Aumentar para 10 segundos

    return () => clearInterval(interval);
  }, [fetchData]);

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const truncateData = (data, maxLength = 100) => {
    if (!data) return 'N/A';
    if (data.length <= maxLength) return data;
    return data.substring(0, maxLength) + '...';
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading">
          <div className="spinner"></div>
          <p>Carregando dados do honeypot...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container">
        <div className="error">
          <h2>❌ Erro de Conexão</h2>
          <p>Não foi possível conectar ao backend: {error}</p>
          <button onClick={() => window.location.reload()}>
            Tentar Novamente
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <header>
        <h1>🍯 Honeypot Monitoring Dashboard</h1>
        <p className="api-info">Conectado em: {currentApiUrl}</p>
        {lastUpdate && (
          <p className="last-update">
            Última atualização: {formatTimestamp(lastUpdate)}
            {isUpdating && <span className="updating"> • Atualizando...</span>}
          </p>
        )}
      </header>

      <div className="stats">
        <div className="stat-card">
          <h3>📊 Total de Tentativas</h3>
          <p className="stat-number">{stats.total_attempts}</p>
        </div>
        <div className="stat-card">
          <h3>🌐 IPs Únicos</h3>
          <p className="stat-number">{stats.unique_ips}</p>
        </div>
        <div className="stat-card">
          <h3>⚡ Status</h3>
          <p className="status-active">Ativo</p>
        </div>
      </div>

      <div className="attempts-section">
        <h2>🚨 Tentativas Recentes</h2>
        
        {attempts.length === 0 ? (
          <div className="no-attempts">
            <p>Nenhuma tentativa registrada ainda.</p>
            <p>O honeypot está aguardando conexões na porta 2222...</p>
          </div>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Endereço IP</th>
                  <th>Dados da Conexão</th>
                  <th>Timestamp</th>
                </tr>
              </thead>
              <tbody>
                {attempts.map(attempt => (
                  <tr key={attempt.id} className="attempt-row">
                    <td className="id-cell">#{attempt.id}</td>
                    <td className="ip-cell">{attempt.ip}</td>
                    <td className="data-cell">
                      <code>{truncateData(attempt.data)}</code>
                    </td>
                    <td className="timestamp-cell">
                      {formatTimestamp(attempt.timestamp)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
