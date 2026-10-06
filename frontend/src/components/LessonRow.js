import React from 'react';

function formatDuration(mins) {
  if (!mins) return '—';
  if (mins < 60) return `${mins} min`;
  const h = Math.floor(mins / 60);
  const m = mins % 60;
  return m > 0 ? `${h}h ${m}min` : `${h}h`;
}

export default function LessonRow({ lesson, onClick }) {
  const isQuiz   = lesson.type === 'quiz';
  const vid      = lesson.video;
  const duration = isQuiz ? '5 min' : formatDuration(vid?.duration_minutes || lesson.duration_minutes);

  return (
    <div className="lesson-row" onClick={onClick} style={{
      display: 'flex', alignItems: 'center', gap: 12,
      padding: '11px 18px', borderBottom: '0.5px solid var(--border)',
      cursor: 'pointer', transition: 'background .15s'
    }}
    onMouseEnter={e => e.currentTarget.style.background = 'var(--bg2)'}
    onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
    >
      {isQuiz ? (
        <div style={{ width: 88, height: 54, borderRadius: 8, background: 'var(--purple-bg)',
          display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 22, flexShrink: 0 }}>
          📝
        </div>
      ) : (
        <div style={{ width: 88, height: 54, borderRadius: 8, background: 'var(--bg3)',
          flexShrink: 0, position: 'relative', overflow: 'hidden' }}>
          {vid && <img src={vid.thumbnail} alt="thumbnail"
            style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }} />}
          <div style={{ position: 'absolute', inset: 0, display: 'flex',
            alignItems: 'center', justifyContent: 'center', background: 'rgba(0,0,0,0.25)' }}>
            <div style={{ width: 26, height: 26, background: 'rgba(0,0,0,0.7)', borderRadius: '50%',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: 10, color: 'white', paddingLeft: 2 }}>▶</div>
          </div>
        </div>
      )}
      <div style={{ flex: 1, minWidth: 0 }}>
        <p style={{ fontSize: 13, fontWeight: 500, marginBottom: 3,
          overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
          {lesson.title}
        </p>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span className={`tag ${isQuiz ? 'tag-purple' : 'tag-blue'}`}>{isQuiz ? 'Quiz' : 'Video'}</span>
          <span style={{ fontSize: 12, color: 'var(--text3)' }}>{duration}</span>
        </div>
        {!isQuiz && vid && (
          <p style={{ fontSize: 11, color: 'var(--text3)', marginTop: 2,
            overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
            ▶ {vid.channel} · {vid.title?.slice(0, 50)}
          </p>
        )}
      </div>
      <span style={{ fontSize: 14, color: 'var(--text3)' }}>›</span>
    </div>
  );
}
