"""
Progress Service — SQLite-backed lesson completion and quiz score tracking
"""
import sqlite3, os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "course_progress.db")


def _get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = _get_connection()
    conn.execute("""CREATE TABLE IF NOT EXISTS course_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id TEXT NOT NULL, course_title TEXT NOT NULL,
        topic TEXT NOT NULL, total_lessons INTEGER NOT NULL,
        total_quizzes INTEGER NOT NULL, created_at TEXT NOT NULL)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS lesson_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id TEXT NOT NULL, module_index INTEGER NOT NULL,
        lesson_index INTEGER NOT NULL, lesson_type TEXT NOT NULL,
        completed INTEGER DEFAULT 0, quiz_score INTEGER,
        quiz_total INTEGER, completed_at TEXT,
        UNIQUE(course_id, module_index, lesson_index))""")
    conn.commit()
    conn.close()


def create_course_record(course_id, course_title, topic, total_lessons, total_quizzes):
    conn = _get_connection()
    conn.execute(
        "INSERT INTO course_progress (course_id,course_title,topic,total_lessons,total_quizzes,created_at) VALUES (?,?,?,?,?,?)",
        (course_id, course_title, topic, total_lessons, total_quizzes, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()


def mark_lesson_complete(course_id, module_index, lesson_index, lesson_type, quiz_score=None, quiz_total=None):
    conn = _get_connection()
    conn.execute(
        """INSERT INTO lesson_progress (course_id,module_index,lesson_index,lesson_type,completed,quiz_score,quiz_total,completed_at)
           VALUES (?,?,?,?,1,?,?,?)
           ON CONFLICT(course_id,module_index,lesson_index)
           DO UPDATE SET completed=1,quiz_score=excluded.quiz_score,quiz_total=excluded.quiz_total,completed_at=excluded.completed_at""",
        (course_id, module_index, lesson_index, lesson_type, quiz_score, quiz_total, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
    return get_course_progress(course_id)


def get_course_progress(course_id):
    conn = _get_connection()
    course = conn.execute("SELECT * FROM course_progress WHERE course_id=?", (course_id,)).fetchone()
    if not course:
        conn.close()
        return {"error": "course not found", "course_id": course_id}
    rows = conn.execute("SELECT * FROM lesson_progress WHERE course_id=? AND completed=1", (course_id,)).fetchall()
    conn.close()

    total_items = course["total_lessons"] + course["total_quizzes"]
    quiz_scores = [{"module": r["module_index"], "lesson": r["lesson_index"],
                    "score": r["quiz_score"], "total": r["quiz_total"]}
                   for r in rows if r["lesson_type"] == "quiz" and r["quiz_score"] is not None]
    avg = None
    if quiz_scores:
        pcts = [q["score"] / q["total"] * 100 for q in quiz_scores if q["total"]]
        avg = round(sum(pcts) / len(pcts)) if pcts else None

    return {"course_id": course_id, "course_title": course["course_title"],
            "topic": course["topic"], "total_items": total_items,
            "completed_items": len(rows),
            "percent_complete": round((len(rows) / total_items) * 100) if total_items else 0,
            "quiz_scores": quiz_scores, "average_quiz_score_pct": avg,
            "completed_lessons": [{"module": r["module_index"], "lesson": r["lesson_index"]} for r in rows]}


def list_courses():
    conn = _get_connection()
    rows = conn.execute("SELECT course_id FROM course_progress ORDER BY created_at DESC").fetchall()
    conn.close()
    return [get_course_progress(r["course_id"]) for r in rows]
