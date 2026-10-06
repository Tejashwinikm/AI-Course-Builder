from flask import Blueprint, request, jsonify
from services.mentor_service import ask_mentor

mentor_bp = Blueprint("mentor", __name__)

@mentor_bp.route("/ask", methods=["POST"])
def ask():
    data = request.get_json() or {}
    topic               = data.get("topic","")
    lesson_title        = data.get("lesson_title","")
    lesson_summary      = data.get("lesson_summary","")
    key_concepts        = data.get("key_concepts",[])
    progress_pct        = int(data.get("progress_pct",0))
    conversation_history = data.get("conversation_history",[])
    user_question       = data.get("question","")
    if not topic or not user_question:
        return jsonify({"error": "topic and question are required"}), 400
    try:
        result = ask_mentor(topic, lesson_title, lesson_summary, key_concepts,
                            progress_pct, conversation_history, user_question)
        return jsonify({"success": True, **result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
