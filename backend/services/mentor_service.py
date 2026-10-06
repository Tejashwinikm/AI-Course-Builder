"""
Mentor Service — Context-Aware AI Chatbot (RAG pattern)
"""
import os
from langchain.prompts import PromptTemplate
from services.ai_service import _safe_text_call

USE_MOCK = os.environ.get("USE_MOCK", "true").lower() == "true"

MENTOR_PROMPT = PromptTemplate(
    input_variables=["topic", "lesson_title", "lesson_summary", "key_concepts",
                      "progress_pct", "conversation_history", "user_question"],
    template="""You are a friendly AI mentor helping a student learn {topic}.
Answer based on the context below — be concise (2-4 sentences) and supportive.

Current lesson: {lesson_title}
Lesson summary: {lesson_summary}
Key concepts: {key_concepts}
Student progress: {progress_pct}% complete

Recent conversation:
{conversation_history}

Student question: {user_question}

Answer directly and encouragingly. Ground your answer in the lesson context above."""
)


def _mock_reply(topic, lesson_title, user_question, key_concepts):
    q = user_question.lower()
    concept = key_concepts[0] if key_concepts else topic
    if any(w in q for w in ["stuck", "confused", "don't understand", "hard"]):
        return (f"No worries — {lesson_title} can feel tricky at first. "
                f"Try focusing just on {concept} for now, and re-watch the relevant video section. "
                f"You're making great progress — keep going!")
    if any(w in q for w in ["why", "what", "how", "explain"]):
        return (f"Good question! In {lesson_title}, {concept} is important because "
                f"it's a core building block in {topic}. "
                f"Re-watching that video section will help reinforce it.")
    return (f"Great question about {topic}. Based on '{lesson_title}', "
            f"I'd suggest reviewing the key concepts and trying a small example yourself.")


def ask_mentor(topic, lesson_title, lesson_summary, key_concepts,
               progress_pct, conversation_history, user_question):
    key_concepts = key_concepts or []
    if USE_MOCK:
        return {"reply": _mock_reply(topic, lesson_title, user_question, key_concepts),
                "grounded": True, "source": "mock"}

    history_text = "\n".join(
        f"{'Student' if t['role'] == 'user' else 'Mentor'}: {t['text']}"
        for t in conversation_history[-6:]
    ) or "(no previous messages)"

    try:
        reply = _safe_text_call(
            MENTOR_PROMPT,
            {"topic": topic, "lesson_title": lesson_title,
             "lesson_summary": lesson_summary or f"Introduction to {lesson_title}",
             "key_concepts": ", ".join(key_concepts) if key_concepts else topic,
             "progress_pct": progress_pct,
             "conversation_history": history_text,
             "user_question": user_question},
            fallback_fn=lambda: _mock_reply(topic, lesson_title, user_question, key_concepts),
            fallback_args=(),
        )
        return {"reply": reply, "grounded": True, "source": "llm"}
    except Exception as e:
        print(f"[Mentor Service] Failed: {e}")
        return {"reply": _mock_reply(topic, lesson_title, user_question, key_concepts),
                "grounded": False, "source": "fallback_error"}
