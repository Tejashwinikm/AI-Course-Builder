import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import ModuleCard from '../components/ModuleCard';
import ProgressBar from '../components/ProgressBar';
import { getProgress } from '../utils/api';

const LEVEL_TAG = { beginner: 'tag-green', intermediate: 'tag-amber', advanced: 'tag-blue' };

export default function CoursePage({ course, onOpenLesson, onBack }) {
  const [progress, setProgress] = useState(null);

  useEffect(() => {
    if (course?.course_id) {
      getProgress(course.course_id)
        .then(res => setProgress(res.data.progress))
        .catch(() => {});
    }
  }, [course]);

  if (!course) return null;
  const levelTag = LEVEL_TAG[course.level] || 'tag-blue';

  return (
    <>
      <Navbar />
      <div style={{ maxWidth: 760, margin: '0 auto', padding: '2rem 1.5rem' }}>
        <button className="btn-ghost" onClick={onBack} style={{ marginBottom: '1.5rem' }}>
          ← New course
        </button>

        <div style={{ marginBottom: '1.75rem' }}>
          <span className={`tag ${levelTag}`} style={{ marginBottom: 8, display: 'inline-block' }}>
            {course.level}
          </span>
          <h1 style={{ fontSize: 26, fontWeight: 700, letterSpacing: '-0.3px', marginBottom: 8 }}>
            {course.course_title}
          </h1>
          <p style={{ fontSize: 14, color: 'var(--text2)', lineHeight: 1.6, marginBottom: '1.25rem' }}>
            {course.course_description}
          </p>
          <div style={{ display: 'flex', gap: '1.5rem', flexWrap: 'wrap', marginBottom: '1.25rem' }}>
            {[
              [course.total_modules,  'Modules'],
              [course.total_videos,   'Lessons'],
              [course.total_quizzes,  'Quizzes'],
              [course.estimated_hours + 'h', 'Est. time'],
            ].map(([n, l]) => (
              <div key={l} style={{ textAlign: 'center' }}>
                <div style={{ fontSize: 22, fontWeight: 700 }}>{n}</div>
                <div style={{ fontSize: 12, color: 'var(--text3)' }}>{l}</div>
              </div>
            ))}
          </div>
        </div>

        {progress && (
          <ProgressBar
            percent={progress.percent_complete}
            completedItems={progress.completed_items}
            totalItems={progress.total_items}
            avgQuizScore={progress.average_quiz_score_pct}
          />
        )}

        {course.modules.map((mod, mi) => (
          <ModuleCard key={mi} module={mod} defaultOpen={mi === 0} onOpenLesson={onOpenLesson} />
        ))}

        <div style={{ marginTop: '1.5rem', padding: '1rem 1.25rem', background: 'var(--bg)',
          border: '0.5px solid var(--border)', borderRadius: 'var(--r-lg)',
          display: 'flex', alignItems: 'center', gap: 12 }}>
          <span style={{ fontSize: 20 }}>🔑</span>
          <div style={{ flex: 1 }}>
            <p style={{ fontSize: 13, fontWeight: 500, marginBottom: 2 }}>Running in mock mode</p>
            <p style={{ fontSize: 12, color: 'var(--text3)' }}>
              Set USE_MOCK=false and add API keys for real AI curriculum and live YouTube search.
            </p>
          </div>
          <button className="btn-outline" onClick={onBack}>New course</button>
        </div>
      </div>
    </>
  );
}
