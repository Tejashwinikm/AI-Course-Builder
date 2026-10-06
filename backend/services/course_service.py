"""
Course Builder Service — Fixed
================================
When USE_MOCK=false + YOUTUBE_API_KEY is set:
  - Searches YouTube LIVE per lesson → no hardcoded IDs → no unavailable videos
When USE_MOCK=true:
  - Uses hardcoded pool as fallback
"""
import os
from services.ai_service import generate_curriculum, generate_quiz, generate_lesson_summary
from services.youtube_service import _find_pool, search_videos

USE_MOCK = os.environ.get("USE_MOCK", "true").lower() == "true"
YOUTUBE_KEY = os.environ.get("YOUTUBE_API_KEY", "")
USE_LIVE_YOUTUBE = not USE_MOCK and bool(YOUTUBE_KEY) and YOUTUBE_KEY != "your_youtube_data_api_v3_key_here"


def build_course(topic: str, level: str = "beginner", num_modules: int = 4) -> dict:

    # Step 1 — AI generates structured curriculum
    curriculum = generate_curriculum(topic, level, num_modules)

    # Step 2 — Get video pool upfront
    # If live YouTube is available → search per module query (fresh, always works)
    # If mock → use hardcoded pool (fast, no API needed)
    if not USE_LIVE_YOUTUBE:
        full_pool = _find_pool(topic)
        pool_index = 0

    enriched_modules = []
    for module in curriculum.get("modules", []):
        queries = module.get("youtube_search_queries", [topic])
        module_query = queries[0] if queries else topic

        enriched_lessons = []
        lesson_videos = []

        # Fetch videos for this module's lessons upfront
        if USE_LIVE_YOUTUBE:
            # Live search: 1 search per module, get enough videos for all lessons
            video_count = len([l for l in module.get("lessons", []) if l["type"] == "video"])
            lesson_videos = search_videos(module_query, max_results=max(video_count, 2))

        live_vid_index = 0

        for lesson in module.get("lessons", []):
            if lesson["type"] == "video":
                if USE_LIVE_YOUTUBE:
                    # Use live YouTube result for this lesson
                    if live_vid_index < len(lesson_videos):
                        video = lesson_videos[live_vid_index]
                        live_vid_index += 1
                    else:
                        # Search specifically for this lesson if pool ran out
                        results = search_videos(f"{topic} {lesson['title']}", max_results=1)
                        video = results[0] if results else None
                else:
                    # Use hardcoded pool
                    entry = full_pool[pool_index % len(full_pool)]
                    pool_index += 1
                    vid_id, vid_title, vid_channel, vid_dur = entry[0], entry[1], entry[2], entry[3]
                    video = {
                        "id": vid_id, "title": vid_title, "channel": vid_channel,
                        "duration_minutes": vid_dur,
                        "thumbnail": f"https://img.youtube.com/vi/{vid_id}/mqdefault.jpg",
                        "embed_url": f"https://www.youtube.com/embed/{vid_id}?rel=0&modestbranding=1"
                    }

                # Update lesson duration from real video if available
                if video and video.get("duration_minutes"):
                    lesson["duration_minutes"] = video["duration_minutes"]

                summary = generate_lesson_summary(
                    topic, lesson["title"], lesson.get("key_concepts", [])
                )
                enriched_lessons.append({**lesson, "video": video, "summary": summary})

            elif lesson["type"] == "quiz":
                all_concepts = [
                    c for l in module.get("lessons", [])
                    if l["type"] == "video"
                    for c in l.get("key_concepts", [])
                ]
                quiz = generate_quiz(
                    topic, module["title"], lesson["title"], all_concepts[:6]
                )
                enriched_lessons.append({**lesson, "quiz": quiz})

        enriched_modules.append({**module, "lessons": enriched_lessons})

    total_videos  = sum(len([l for l in m["lessons"] if l["type"] == "video"]) for m in enriched_modules)
    total_quizzes = sum(len([l for l in m["lessons"] if l["type"] == "quiz"])  for m in enriched_modules)

    return {
        "topic": topic, "level": level,
        "course_title":       curriculum.get("course_title", topic),
        "course_description": curriculum.get("course_description", ""),
        "estimated_hours":    curriculum.get("estimated_hours", num_modules * 2),
        "total_modules":      len(enriched_modules),
        "total_videos":       total_videos,
        "total_quizzes":      total_quizzes,
        "modules":            enriched_modules,
        "mode": "live" if USE_LIVE_YOUTUBE else "mock"
    }