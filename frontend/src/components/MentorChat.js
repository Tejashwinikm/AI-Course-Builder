import React, { useState, useRef, useEffect } from 'react';
import { askMentor } from '../utils/api';

export default function MentorChat({ topic, lessonTitle, lessonSummary, keyConcepts, progressPct }) {
  const [open,    setOpen]    = useState(false);
  const [history, setHistory] = useState([]);
  const [input,   setInput]   = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [history]);

  async function send() {
    const q = input.trim();
    if (!q || loading) return;
    setInput('');
    const newHistory = [...history, { role: 'user', text: q }];
    setHistory(newHistory);
    setLoading(true);
    try {
      const res = await askMentor(topic, lessonTitle, lessonSummary, keyConcepts,
                                   progressPct, newHistory, q);
      setHistory(h => [...h, { role: 'mentor', text: res.data.reply }]);
    } catch {
      setHistory(h => [...h, { role: 'mentor', text: 'Sorry, I could not connect. Make sure Flask is running.' }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card" style={{ marginBottom: '1.25rem' }}>
      <div onClick={() => setOpen(o => !o)} style={{ display: 'flex', alignItems: 'center',
        justifyContent: 'space-between', cursor: 'pointer' }}>
        <h4 style={{ margin: 0 }}>🤖 AI Mentor Chat</h4>
        <span style={{ fontSize: 13, color: 'var(--text3)' }}>{open ? '▲ Hide' : '▼ Ask a question'}</span>
      </div>

      {open && (
        <div style={{ marginTop: '1rem' }}>
          {history.length === 0 && (
            <p style={{ fontSize: 13, color: 'var(--text3)', marginBottom: 12 }}>
              Ask me anything about this lesson — I'm here to help!
            </p>
          )}

          {history.length > 0 && (
            <div className="chat-wrap">
              {history.map((msg, i) => (
                <div key={i} className={`chat-bubble ${msg.role}`}>{msg.text}</div>
              ))}
              {loading && (
                <div className="chat-bubble mentor" style={{ opacity: 0.6 }}>
                  <span>Thinking</span>
                  <span style={{ animation: 'pulse 1s infinite' }}>...</span>
                </div>
              )}
              <div ref={bottomRef} />
            </div>
          )}

          <div className="chat-input-row">
            <input
              type="text" value={input} placeholder="Ask a question about this lesson..."
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && send()}
              disabled={loading}
            />
            <button className="btn-sm" onClick={send} disabled={loading || !input.trim()}>
              {loading ? '...' : 'Ask'}
            </button>
          </div>

          <div style={{ marginTop: 10, display: 'flex', flexWrap: 'wrap', gap: 6 }}>
            {["Can you explain this concept?", "I'm stuck, can you help?", "Give me a practical example"].map(q => (
              <button key={q} onClick={() => setInput(q)} style={{
                background: 'var(--bg2)', border: '0.5px solid var(--border2)',
                borderRadius: 100, padding: '3px 10px', fontSize: 11,
                color: 'var(--text2)', cursor: 'pointer', fontFamily: 'inherit'
              }}>{q}</button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
