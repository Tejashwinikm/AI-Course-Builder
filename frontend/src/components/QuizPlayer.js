import React, { useState } from 'react';

export default function QuizPlayer({ quiz, mi, li, onBack }) {
  const questions = quiz?.questions || [];
  const [index,  setIndex]  = useState(0);
  const [score,  setScore]  = useState(0);
  const [chosen, setChosen] = useState(null);
  const [done,   setDone]   = useState(false);

  if (!questions.length) return <p style={{ color: 'var(--text3)' }}>No quiz data available.</p>;

  const q      = questions[index];
  const total  = questions.length;
  const isLast = index === total - 1;
  const pct    = Math.round((score / total) * 100);

  function answer(i) {
    if (chosen !== null) return;
    setChosen(i);
    if (i === q.correct_index) setScore(s => s + 1);
  }

  function next() {
    if (isLast) setDone(true);
    else { setIndex(i => i + 1); setChosen(null); }
  }

  if (done) {
    const pass = pct >= 70;
    return (
      <div style={{ textAlign: 'center', padding: '2rem 0' }}>
        <div style={{ width: 80, height: 80, borderRadius: '50%', margin: '0 auto 1.25rem',
          background: pass ? 'var(--green-bg)' : 'var(--amber-bg)',
          color: pass ? 'var(--green)' : 'var(--amber)',
          display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
          <span style={{ fontSize: 26, fontWeight: 700 }}>{pct}%</span>
          <span style={{ fontSize: 11 }}>{score}/{total}</span>
        </div>
        <h2 style={{ fontSize: 22, fontWeight: 600, marginBottom: 8 }}>{pass ? 'Well done!' : 'Keep going!'}</h2>
        <p style={{ color: 'var(--text2)', fontSize: 14, marginBottom: '1.5rem' }}>
          {pass ? 'You passed this quiz!' : 'Review the lessons and try again.'}
        </p>
        <div style={{ display: 'flex', gap: 10, justifyContent: 'center' }}>
          <button className="btn-outline" onClick={() => { setIndex(0); setScore(0); setChosen(null); setDone(false); }}>
            Retake quiz
          </button>
          <button className="btn-sm" onClick={onBack}>Continue course →</button>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12,
          color: 'var(--text3)', marginBottom: 6 }}>
          <span>Question {index + 1} of {total}</span>
          <span>{score} correct so far</span>
        </div>
        <div className="progress-wrap">
          <div className="progress-bar" style={{ width: `${((index + 1) / total) * 100}%` }} />
        </div>
      </div>
      <p style={{ fontSize: 16, fontWeight: 500, marginBottom: '1.25rem', lineHeight: 1.5 }}>{q.question}</p>
      <div style={{ marginBottom: '1.25rem' }}>
        {q.options.map((opt, i) => {
          let cls = 'quiz-opt';
          if (chosen !== null) {
            if (i === q.correct_index) cls += ' correct';
            else if (i === chosen) cls += ' wrong';
            cls += ' disabled';
          }
          return (
            <div key={i} className={cls} onClick={() => answer(i)}>
              <div className="opt-letter">{'ABCD'[i]}</div>
              <span>{opt}</span>
            </div>
          );
        })}
      </div>
      {chosen !== null && (
        <>
          <div style={{ padding: '12px 16px', borderRadius: 'var(--r)', fontSize: 14, marginBottom: '1.25rem',
            background: chosen === q.correct_index ? 'var(--green-bg)' : 'var(--red-bg)',
            color:      chosen === q.correct_index ? 'var(--green)'    : 'var(--red)' }}>
            <strong>{chosen === q.correct_index ? '✓ Correct!' : '✗ Not quite.'}</strong>
            {q.explanation && <><br /><span style={{ fontSize: 13 }}>{q.explanation}</span></>}
          </div>
          <button className="btn-sm" onClick={next}>
            {isLast ? 'See results →' : 'Next question →'}
          </button>
        </>
      )}
    </div>
  );
}
