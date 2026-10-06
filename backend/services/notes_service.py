"""
Notes Service — Transcript-Grounded AI Note Generation (RAG)
"""
import os
from langchain.prompts import PromptTemplate
from services.ai_service import _safe_text_call

USE_MOCK = os.environ.get("USE_MOCK", "true").lower() == "true"

NOTES_PROMPT = PromptTemplate(
    input_variables=["topic", "lesson_title", "transcript_excerpt"],
    template="""You are a study notes assistant. Using ONLY the video transcript excerpt below,
write structured study notes for this lesson.

Topic: {topic}
Lesson: {lesson_title}

Transcript excerpt:
\"\"\"{transcript_excerpt}\"\"\"

Write 4-6 bullet points covering key ideas from the transcript. Start each line with "- ".
Plain text only. Do not invent information not in the transcript."""
)


def _fetch_transcript(video_id: str, max_chars: int = 4000) -> str:
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
        text = " ".join(entry["text"] for entry in transcript_list)
        return text[:max_chars]
    except Exception as e:
        print(f"[Notes Service] Transcript unavailable for {video_id}: {type(e).__name__}")
        return ""


def _mock_notes(topic: str, lesson_title: str, key_concepts: list) -> dict:
    concepts = (key_concepts + [topic, "core principles", "practical use"])[:3]
    return {"lesson_title": lesson_title, "source": "mock", "grounded_in_transcript": False,
            "notes": [
                f"{lesson_title} introduces the core ideas behind {concepts[0]}.",
                f"Key concept: understanding how {concepts[0]} fits into the broader {topic} workflow.",
                f"Practical example: applying {concepts[1]} in a real scenario.",
                f"Common mistake to avoid: skipping fundamentals before moving to advanced {topic} topics.",
                f"Takeaway: practice {concepts[2]} hands-on to reinforce the lesson.",
            ]}


def generate_notes(topic: str, lesson_title: str, video_id: str, key_concepts: list = None) -> dict:
    key_concepts = key_concepts or []
    if USE_MOCK:
        return _mock_notes(topic, lesson_title, key_concepts)

    transcript = _fetch_transcript(video_id)
    if not transcript:
        result = _mock_notes(topic, lesson_title, key_concepts)
        result["source"] = "fallback_no_transcript"
        return result

    try:
        raw = _safe_text_call(
            NOTES_PROMPT,
            {"topic": topic, "lesson_title": lesson_title, "transcript_excerpt": transcript},
            fallback_fn=lambda: "\n".join(_mock_notes(topic, lesson_title, key_concepts)["notes"]),
            fallback_args=(),
        )
        bullets = [line.strip("- ").strip() for line in raw.strip().split("\n") if line.strip()]
        return {"lesson_title": lesson_title, "notes": bullets[:8],
                "source": "transcript_rag", "grounded_in_transcript": True}
    except Exception as e:
        print(f"[Notes Service] Generation failed: {e}")
        result = _mock_notes(topic, lesson_title, key_concepts)
        result["source"] = "fallback_error"
        return result
