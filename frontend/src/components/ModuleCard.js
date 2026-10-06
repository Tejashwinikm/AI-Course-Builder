import React, { useState } from 'react';
import LessonRow from './LessonRow';

export default function ModuleCard({ module, defaultOpen, onOpenLesson }) {
  const [open, setOpen] = useState(defaultOpen || false);
  const videos  = module.lessons.filter(l => l.type === 'video').length;
  const quizzes = module.lessons.filter(l => l.type === 'quiz').length;

  return (
    <div style={{ background: 'var(--bg)', border: '0.5px solid var(--border)',
      borderRadius: 'var(--r-lg)', marginBottom: 10, overflow: 'hidden', boxShadow: 'var(--shadow)' }}>
      <div onClick={() => setOpen(o => !o)} style={{
        display: 'flex', alignItems: 'center', gap: 12,
        padding: '14px 18px', cursor: 'pointer',
        background: open ? 'var(--bg2)' : 'var(--bg)', transition: 'background .15s'
      }}>
        <div style={{ width: 34, height: 34, borderRadius: 8, background: 'var(--bg3)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontWeight: 600, fontSize: 13, color: 'var(--text2)', flexShrink: 0 }}>
          {module.module_number}
        </div>
        <div style={{ flex: 1 }}>
          <p style={{ fontSize: 14, fontWeight: 500, marginBottom: 2 }}>{module.title}</p>
          <p style={{ fontSize: 12, color: 'var(--text3)' }}>
            {videos} video{videos !== 1 ? 's' : ''} · {quizzes} quiz
          </p>
        </div>
        <span style={{ fontSize: 14, color: 'var(--text3)', transition: 'transform .2s',
          transform: open ? 'rotate(180deg)' : 'none' }}>▼</span>
      </div>
      {open && (
        <div style={{ borderTop: '0.5px solid var(--border)' }}>
          {module.lessons.map((lesson, li) => (
            <LessonRow key={li} lesson={lesson}
              onClick={() => onOpenLesson(module.module_number - 1, li)} />
          ))}
        </div>
      )}
    </div>
  );
}
