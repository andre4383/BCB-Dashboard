import { useEffect, useState } from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, ReferenceLine
} from 'recharts';
import { Activity } from 'lucide-react';
import './index.css';

function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/dados')
      .then((res) => res.json())
      .then((jsonData) => {
        setData(jsonData);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Erro ao buscar dados:", err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="loading-container">
        <Activity className="spinner" size={32} />
      </div>
    );
  }

  const chartData = data.map(item => {
    const dateStr = item.datatrimestre ? item.datatrimestre.split('T')[0] : '';
    return {
      trimestre: dateStr,
      volumeTotalBilhões: ((item.valorPix || 0) + (item.valorTED || 0) + (item.valorCartaoCredito || 0) + (item.valorBoleto || 0)) / 1000000000,
      qtdSaques: item.quantidadeSaques,
      qtdPix: item.quantidadePix,
      valorPixBilhões: (item.valorPix || 0) / 1000000000,
      valorTEDBilhões: (item.valorTED || 0) / 1000000000,
    };
  });

  return (
    <div className="app-layout">
      <main className="main-content">
        <header style={{ justifyContent: 'center', padding: '1.5rem', borderBottom: '1px solid var(--surface-border)' }}>
          <div className="header-left" style={{ fontSize: '1.2rem' }}>
            <span style={{ fontWeight: 600 }}>Projeto Banco Central do Brasil</span>
            <span style={{ color: '#cbd5e1', margin: '0 12px' }}>|</span>
            <span style={{ color: '#64748b', fontWeight: 400 }}>Análise de Meios de Pagamento</span>
          </div>
        </header>

        <div className="dashboard-container" style={{ maxWidth: '1000px', margin: '0 auto', width: '100%', paddingTop: '3rem' }}>
          <div className="welcome-section" style={{ marginBottom: '3rem', textAlign: 'center' }}>
            <h2 style={{ fontSize: '2.5rem', marginBottom: '0.5rem', fontWeight: 600 }}>Análise de Meios de Pagamento no Brasil</h2>
            <p style={{ fontSize: '1.1rem' }}>Evolução histórica de pagamentos com base nos dados do Banco Central</p>
          </div>

          {/* Report Section 1 */}
          <div className="report-section">
            <h3>Evolução do Volume Financeiro</h3>
            <p className="report-paragraph">
              O gráfico apresenta o crescimento contínuo do volume financeiro total transacionado eletronicamente (somatório de Pix, TED, Cartões e Boletos) por trimestre, evidenciando o aumento do fluxo financeiro em canais digitais ao longo do período analisado.
            </p>
            <div className="chart-container" style={{ width: '100%', height: 350 }}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                  <XAxis dataKey="trimestre" stroke="#cbd5e1" tick={{ fill: '#94a3b8', fontSize: 11 }} axisLine={false} tickLine={false} />
                  <YAxis stroke="#cbd5e1" tick={{ fill: '#94a3b8', fontSize: 11 }} axisLine={false} tickLine={false} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#ffffff', borderRadius: '8px', border: '1px solid #f1f5f9', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.05)' }}
                  />
                  <Line type="monotone" dataKey="volumeTotalBilhões" name="Volume Total (Bilhões R$)" stroke="#0f172a" strokeWidth={2} dot={false} activeDot={{ r: 4, fill: '#0f172a' }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Report Section 2 */}
          <div className="report-section">
            <h3>Declínio de Saques em Espécie</h3>
            <p className="report-paragraph">
              A quantidade de saques apresenta uma tendência histórica de queda. A análise divide o período em 5 partes: (1) Era Tradicional pré-2017, (2) Crescimento dos Bancos Digitais, (3) Choque da Pandemia, (4) Lançamento do Pix e (5) Consolidação do Pagamento Instantâneo.
            </p>
            <div className="chart-container" style={{ width: '100%', height: 350 }}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData} margin={{ top: 20, right: 10, left: 10, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                  <XAxis dataKey="trimestre" stroke="#cbd5e1" tick={{ fill: '#94a3b8', fontSize: 11 }} axisLine={false} tickLine={false} />
                  <YAxis stroke="#cbd5e1" tick={{ fill: '#94a3b8', fontSize: 11 }} axisLine={false} tickLine={false} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#ffffff', borderRadius: '8px', border: '1px solid #f1f5f9', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.05)' }}
                  />
                  <ReferenceLine x="2017-03-31" stroke="#8b5cf6" strokeDasharray="3 3" label={{ value: 'Bancos Digitais', position: 'insideTopLeft', fill: '#8b5cf6', fontSize: 11 }} />
                  <ReferenceLine x="2020-03-31" stroke="#ef4444" strokeDasharray="3 3" label={{ value: 'Pandemia', position: 'insideTopLeft', fill: '#ef4444', fontSize: 11 }} />
                  <ReferenceLine x="2020-12-31" stroke="#10b981" strokeDasharray="3 3" label={{ value: 'Lançamento Pix', position: 'insideTopLeft', fill: '#10b981', fontSize: 11 }} />
                  <ReferenceLine x="2022-03-31" stroke="#f59e0b" strokeDasharray="3 3" label={{ value: 'Consolidação', position: 'insideTopLeft', fill: '#f59e0b', fontSize: 11 }} />
                  <Line type="monotone" dataKey="qtdSaques" name="Qtd. de Saques" stroke="#94a3b8" strokeWidth={2} dot={false} activeDot={{ r: 4, fill: '#94a3b8' }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Report Section 3 */}
          <div className="report-section">
            <h3>TED: Crescimento e Estagnação</h3>
            <p className="report-paragraph">
              A Transferência Eletrônica Disponível (TED) apresentou períodos de expansão, porém demonstra estagnação em seu volume financeiro após a introdução de novos meios de pagamento.
            </p>
            <div className="chart-container" style={{ width: '100%', height: 350 }}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData} margin={{ top: 20, right: 10, left: 10, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                  <XAxis dataKey="trimestre" stroke="#cbd5e1" tick={{ fill: '#94a3b8', fontSize: 11 }} axisLine={false} tickLine={false} />
                  <YAxis stroke="#cbd5e1" tick={{ fill: '#94a3b8', fontSize: 11 }} axisLine={false} tickLine={false} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#ffffff', borderRadius: '8px', border: '1px solid #f1f5f9', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.05)' }}
                  />
                  <ReferenceLine x="2020-11-01" stroke="red" strokeDasharray="3 3" label={{ value: 'Lançamento do Pix', position: 'insideTopLeft', fill: 'red', fontSize: 11 }} />
                  <Line type="monotone" dataKey="valorTEDBilhões" name="Volume TED (Bilhões R$)" stroke="#0f172a" strokeWidth={2} dot={false} activeDot={{ r: 4, fill: '#0f172a' }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </main >
    </div >
  );
}

export default App;
