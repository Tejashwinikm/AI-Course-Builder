import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import QuizPlayer from '../components/QuizPlayer';
import NotesPanel from '../components/NotesPanel';
import MentorChat from '../components/MentorChat';
import { completeLesson } from '../utils/api';

export default function LessonPage({ course, mi, li, onBack, onOpenLesson }) {
  const mod    = course.modules[mi];
  const lesson = mod.lessons[li];
  const isQuiz = lesson.type === 'quiz';
  const vid    = lesson.video;
  const [marked, setMarked] = useState(false);

  async function markComplete(quizScore = null, quizTotal = null) {
    if (!course.course_id || marked) return;
    try {
      await completeLesson(course.course_id, mi, li, lesson.type, quizScore, quizTotal);
      setMarked(true);
    } catch { /* optional */ }
  }

  function goNext() {
    if (li < mod.lessons.length - 1) onOpenLesson(mi, li + 1);
    else if (mi < course.modules.length - 1) onOpenLesson(mi + 1, 0);
    else onBack();
  }
  function goPrev() {
    if (li > 0) onOpenLesson(mi, li - 1);
    else if (mi > 0) { const p = course.modules[mi - 1]; onOpenLesson(mi - 1, p.lessons.length - 1); }
    else onBack();
  }

  return (
    <>
      <Navbar />
      <div style={{ maxWidth: 760, margin: '0 auto', padding: '2rem 1.5rem' }}>
        <button className="btn-ghost" onClick={onBack} style={{ marginBottom: '1.5rem' }}>
          ← Back to course
        </button>

        <div style={{ marginBottom: '1.25rem' }}>
          <span className={`tag ${isQuiz ? 'tag-purple' : 'tag-blue'}`}
            style={{ marginBottom: 8, display: 'inline-block' }}>
            Module {mi + 1}: {mod.title}
          </span>
          <h2 style={{ fontSize: 22, fontWeight: 600, marginBottom: 4 }}>{lesson.title}</h2>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <p style={{ fontSize: 13, color: 'var(--text3)' }}>
              {isQuiz ? '5 min · Quiz' : `${vid?.duration_minutes || lesson.duration_minutes} min · Video lesson`}
            </p>
            {marked && <span className="tag tag-green">✓ Completed</span>}
          </div>
        </div>

        {isQuiz ? (
          <div className="card">
            <QuizPlayer quiz={lesson.quiz} mi={mi} li={li} onBack={onBack} />
          </div>
        ) : (
          <>
            {vid ? (
              <>
                <div className="video-frame" style={{ marginBottom: '1.25rem' }}
                  onMouseEnter={() => markComplete()}>
                  <iframe src={vid.embed_url} allowFullScreen title={lesson.title} />
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '10px 14px',
                  background: 'var(--bg2)', borderRadius: 'var(--r)', marginBottom: '1.25rem', fontSize: 13 }}>
                  <span style={{ color: '#c00', fontSize: 16 }}>▶</span>
                  <span style={{ flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {vid.title}
                  </span>
                  <a href={`https://youtube.com/watch?v=${vid.id}`} target="_blank" rel="noreferrer"
                    style={{ color: 'var(--blue)', fontSize: 12, textDecoration: 'none', flexShrink: 0 }}>
                    YouTube ↗
                  </a>
                </div>
              </>
            ) : (
              <div className="card" style={{ marginBottom: '1.25rem' }}>
                <p style={{ color: 'var(--text3)' }}>No video found — add a YouTube API key and set USE_MOCK=false.</p>
              </div>
            )}

            {lesson.summary && (
              <div className="card" style={{ marginBottom: '1.25rem' }}>
                <h4>Lesson summary</h4>
                <p style={{ fontSize: 14, color: 'var(--text2)', lineHeight: 1.7 }}>{lesson.summary}</p>
              </div>
            )}

            {lesson.key_concepts?.length > 0 && (
              <div className="card" style={{ marginBottom: '1.25rem' }}>
                <h4>Key concepts</h4>
                <ul style={{ paddingLeft: '1.25rem', fontSize: 14, color: 'var(--text2)', lineHeight: 2 }}>
                  {lesson.key_concepts.map((c, i) => <li key={i}>{c}</li>)}
                </ul>
              </div>
            )}

            {/* Notes Panel */}
            <NotesPanel
              topic={course.topic}
              lessonTitle={lesson.title}
              videoId={vid?.id || ''}
              keyConcepts={lesson.key_concepts || []}
            />

            {/* AI Mentor Chat */}
            <MentorChat
              topic={course.topic}
              lessonTitle={lesson.title}
              lessonSummary={lesson.summary || ''}
              keyConcepts={lesson.key_concepts || []}
              progressPct={0}
            />

            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '1.25rem' }}>
              <button className="btn-ghost" onClick={goPrev}>← Previous</button>
              <button className="btn-sm" onClick={() => { markComplete(); goNext(); }}>
                Mark complete & Next →
              </button>
            </div>
          </>
        )}
      </div>
    </>
  );
}
