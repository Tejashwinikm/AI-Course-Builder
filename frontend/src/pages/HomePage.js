import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import { generateCourse, registerCourse } from '../utils/api';

const QUICK = ['Python Programming','Machine Learning','React & JavaScript','Data Science','Flask & LangChain','System Design'];
const STEPS  = [
  'Designing curriculum with LangChain...',
  'Structuring modules and lessons...',
  'Searching YouTube for resources...',
  'Generating quiz questions with AI...',
  'Assembling your course...',
];

export default function HomePage({ onCourseGenerated }) {
  const [topic,      setTopic]      = useState('');
  const [level,      setLevel]      = useState('beginner');
  const [numModules, setNumModules] = useState(4);
  const [loading,    setLoading]    = useState(false);
  const [stepIdx,    setStepIdx]    = useState(0);
  const [progress,   setProgress]   = useState(0);
  const [error,      setError]      = useState('');

  async function handleGenerate() {
    if (!topic.trim()) return;
    setLoading(true); setError('');

    let si = 0;
    const iv = setInterval(() => {
      si++;
      setStepIdx(si);
      setProgress(Math.min(90, si * 20));
      if (si >= STEPS.length - 1) clearInterval(iv);
    }, 800);

    try {
      const res  = await generateCourse(topic.trim(), level, numModules);
      const course = res.data.course;

      // Register course for progress tracking
      const courseId = `course-${Date.now()}`;
      try {
        await registerCourse(courseId, course.course_title, topic.trim(),
                             course.total_videos, course.total_quizzes);
        course.course_id = courseId;
      } catch { /* progress tracking optional */ }

      clearInterval(iv);
      setProgress(100);
      setTimeout(() => onCourseGenerated(course), 300);
    } catch (e) {
      clearInterval(iv);
      setError(e.response?.data?.error || 'Failed to generate course. Is the Flask server running on port 5000?');
      setLoading(false); setProgress(0); setStepIdx(0);
    }
  }

  return (
    <>
      <Navbar />
      <div style={{ maxWidth: 600, margin: '4rem auto', padding: '0 1.5rem' }}>
        {/* Hero */}
        <div style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
          <div style={{ display: 'inline-block', background: 'var(--bg3)',
            border: '0.5px solid var(--border2)', borderRadius: 100,
            padding: '5px 16px', fontSize: 13, color: 'var(--text2)', marginBottom: '1.25rem' }}>
            🤖 React + Flask + Python + LangChain
          </div>
          <h1 style={{ fontSize: 34, fontWeight: 700, letterSpacing: '-0.5px', marginBottom: 10 }}>
            Learn anything, instantly
          </h1>
          <p style={{ fontSize: 16, color: 'var(--text2)' }}>
            Type a topic — AI designs a full structured course with YouTube videos, quizzes, notes and a mentor chatbot.
          </p>
        </div>

        {!loading ? (
          <div className="card">
            <div className="field">
              <label>What do you want to learn?</label>
              <input type="text" value={topic}
                placeholder="e.g. Python, Machine Learning, Cooking, React..."
                onChange={e => setTopic(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleGenerate()} />
            </div>
            <div className="field-row">
              <div className="field">
                <label>Level</label>
                <select value={level} onChange={e => setLevel(e.target.value)}>
                  <option value="beginner">Beginner</option>
                  <option value="intermediate">Intermediate</option>
                  <option value="advanced">Advanced</option>
                </select>
              </div>
              <div className="field">
                <label>Modules</label>
                <select value={numModules} onChange={e => setNumModules(+e.target.value)}>
                  {[2, 3, 4, 5].map(n => <option key={n} value={n}>{n} modules</option>)}
                </select>
              </div>
            </div>
            <div style={{ marginBottom: '1.25rem' }}>
              <p style={{ fontSize: 12, color: 'var(--text3)', marginBottom: 8 }}>Quick topics:</p>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                {QUICK.map(t => (
                  <button key={t} onClick={() => setTopic(t)} style={{
                    background: 'var(--bg2)', border: '0.5px solid var(--border2)',
                    borderRadius: 100, padding: '4px 12px', fontSize: 12,
                    color: 'var(--text2)', cursor: 'pointer', fontFamily: 'inherit'
                  }}>{t}</button>
                ))}
              </div>
            </div>
            {error && (
              <div style={{ padding: '10px 14px', background: 'var(--red-bg)', color: 'var(--red)',
                borderRadius: 'var(--r)', fontSize: 13, marginBottom: '1rem' }}>
                {error}
              </div>
            )}
            <button className="btn-primary" style={{ width: '100%', fontSize: 15, padding: 13 }}
              onClick={handleGenerate} disabled={!topic.trim()}>
              ⚡ Generate my course
            </button>
          </div>
        ) : (
          <div className="card" style={{ textAlign: 'center', padding: '2.5rem 2rem' }}>
            <div className="spinner" />
            <h2 style={{ fontSize: 18, fontWeight: 500, marginBottom: 8 }}>
              {STEPS[Math.min(stepIdx, STEPS.length - 1)]}
            </h2>
            <p style={{ fontSize: 13, color: 'var(--text2)', marginBottom: '1.25rem' }}>
              Building "{topic}" · {level} level
            </p>
            <div className="progress-wrap" style={{ marginBottom: '1.5rem' }}>
              <div className="progress-bar" style={{ width: `${progress}%` }} />
            </div>
            <div style={{ textAlign: 'left' }}>
              {STEPS.slice(0, stepIdx + 1).map((s, i) => (
                <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 8,
                  padding: '5px 0', fontSize: 13, color: 'var(--text2)' }}>
                  <span style={{ color: '#639922' }}>✓</span> {s}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Stack info */}
        <div style={{ marginTop: '2rem', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
          {[
            ['⚛️ React',        'Professional UI layer'],
            ['🐍 Flask',        'Python backend & API'],
            ['🔗 LangChain',    'AI prompt orchestration'],
            ['🎬 YouTube API',  'Curated tutorial videos'],
            ['📝 Notes (RAG)',  'Transcript-grounded notes'],
            ['🤖 AI Mentor',   'Context-aware chatbot'],
          ].map(([icon, desc]) => (
            <div key={icon} style={{ padding: '12px 16px', background: 'var(--bg)',
              border: '0.5px solid var(--border)', borderRadius: 'var(--r)',
              display: 'flex', alignItems: 'center', gap: 10 }}>
              <span style={{ fontSize: 18 }}>{icon.split(' ')[0]}</span>
              <div>
                <p style={{ fontSize: 12, fontWeight: 500 }}>{icon.split(' ').slice(1).join(' ')}</p>
                <p style={{ fontSize: 11, color: 'var(--text3)' }}>{desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}
