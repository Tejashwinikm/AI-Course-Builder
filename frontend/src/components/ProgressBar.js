import React from 'react';

export default function ProgressBar({ percent, completedItems, totalItems, avgQuizScore }) {
  return (
    <div style={{ background: 'var(--bg)', border: '0.5px solid var(--border)',
      borderRadius: 'var(--r-lg)', padding: '14px 18px', marginBottom: 16,
      display: 'flex', alignItems: 'center', gap: 16, flexWrap: 'wrap' }}>
      <div style={{ flex: 1, minWidth: 200 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between',
          fontSize: 12, color: 'var(--text2)', marginBottom: 6 }}>
          <span>Course progress</span>
          <span style={{ fontWeight: 600, color: 'var(--text)' }}>{percent}%</span>
        </div>
        <div className="progress-wrap">
          <div className="progress-bar" style={{ width: `${percent}%` }} />
        </div>
        <p style={{ fontSize: 11, color: 'var(--text3)', marginTop: 4 }}>
          {completedItems} of {totalItems} items completed
        </p>
      </div>
      {avgQuizScore !== null && avgQuizScore !== undefined && (
        <div style={{ textAlign: 'center', flexShrink: 0 }}>
          <div style={{ fontSize: 20, fontWeight: 700,
            color: avgQuizScore >= 70 ? 'var(--green)' : 'var(--amber)' }}>
            {avgQuizScore}%
          </div>
          <div style={{ fontSize: 11, color: 'var(--text3)' }}>Avg quiz score</div>
        </div>
      )}
    </div>
  );
}
