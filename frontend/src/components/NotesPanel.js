import React, { useState } from 'react';
import { generateNotes } from '../utils/api';

export default function NotesPanel({ topic, lessonTitle, videoId, keyConcepts }) {
  const [notes,   setNotes]   = useState(null);
  const [loading, setLoading] = useState(false);
  const [error,   setError]   = useState('');

  async function fetchNotes() {
    setLoading(true); setError('');
    try {
      const res = await generateNotes(topic, lessonTitle, videoId, keyConcepts);
      setNotes(res.data);
    } catch (e) {
      setError('Could not generate notes. Make sure Flask is running.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card" style={{ marginBottom: '1.25rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: notes ? '1rem' : 0 }}>
        <h4 style={{ margin: 0 }}>📝 AI Study Notes</h4>
        {!notes && (
          <button className="btn-sm" onClick={fetchNotes} disabled={loading} style={{ fontSize: 12 }}>
            {loading ? 'Generating...' : 'Generate notes'}
          </button>
        )}
        {notes && (
          <button className="btn-outline" onClick={() => setNotes(null)} style={{ fontSize: 11, padding: '4px 10px' }}>
            Regenerate
          </button>
        )}
      </div>

      {error && <p style={{ color: 'var(--red)', fontSize: 13, marginTop: 8 }}>{error}</p>}

      {loading && (
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginTop: 10 }}>
          <div className="spinner" style={{ width: 20, height: 20, margin: 0 }} />
          <span style={{ fontSize: 13, color: 'var(--text2)' }}>
            {notes?.source === 'transcript_rag' ? 'Fetching transcript & generating notes...' : 'Generating notes...'}
          </span>
        </div>
      )}

      {notes && !loading && (
        <>
          <ul style={{ paddingLeft: '1.25rem', fontSize: 14, color: 'var(--text2)', lineHeight: 2 }}>
            {notes.notes?.map((note, i) => <li key={i}>{note}</li>)}
          </ul>
          {notes.grounded_in_transcript && (
            <p style={{ fontSize: 11, color: 'var(--green)', marginTop: 8 }}>
              ✓ Grounded in video transcript
            </p>
          )}
        </>
      )}

      {!notes && !loading && !error && (
        <p style={{ fontSize: 13, color: 'var(--text3)', marginTop: 8 }}>
          Click "Generate notes" to get AI-powered study notes for this lesson.
        </p>
      )}
    </div>
  );
}
