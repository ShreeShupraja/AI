import { useEffect, useState } from 'react';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export default function App() {
  const [health, setHealth] = useState('checking...');
  const [analysisMsg, setAnalysisMsg] = useState('');

  useEffect(() => {
    fetch(`${API_BASE_URL}/healthz`)
      .then((res) => res.json())
      .then((data) => setHealth(`${data.status} (${data.service})`))
      .catch(() => setHealth('unreachable'));
  }, []);

  async function runDemoAnalysis() {
    const response = await fetch(`${API_BASE_URL}/analysis/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ dataset_name: 'demo.csv', quantum_enabled: true })
    });

    if (!response.ok) {
      setAnalysisMsg('Analysis failed. Check API logs.');
      return;
    }

    const data = await response.json();
    setAnalysisMsg(`Run ${data.run_id}: ${data.anomalies_found} anomalies found (${data.status}).`);
  }

  return (
    <main style={{ fontFamily: 'Inter, system-ui, sans-serif', padding: '2rem', background: '#0f172a', minHeight: '100vh', color: '#e2e8f0' }}>
      <h1>🛡️ Quantum Sentinel MVP</h1>
      <p>AI + Quantum anomaly detection starter scaffold.</p>
      <section style={{ marginTop: '1rem', padding: '1rem', border: '1px solid #334155', borderRadius: 12 }}>
        <h2>API Health</h2>
        <p><strong>{health}</strong></p>
        <p style={{ opacity: 0.8 }}>Backend URL: {API_BASE_URL}</p>
      </section>

      <section style={{ marginTop: '1rem', padding: '1rem', border: '1px solid #334155', borderRadius: 12 }}>
        <h2>Demo Analysis</h2>
        <button onClick={runDemoAnalysis} style={{ padding: '0.5rem 0.8rem', borderRadius: 8, cursor: 'pointer' }}>
          Run Quantum Demo
        </button>
        {analysisMsg && <p style={{ marginTop: '0.75rem' }}>{analysisMsg}</p>}
      </section>
    </main>
  );
}
