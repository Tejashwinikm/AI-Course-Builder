from flask import Blueprint, request, jsonify
from services.notes_service import generate_notes

notes_bp = Blueprint("notes", __name__)

@notes_bp.route("/generate", methods=["POST"])
def generate():
    data = request.get_json() or {}
    topic, lesson_title = data.get("topic",""), data.get("lesson_title","")
    video_id, key_concepts = data.get("video_id",""), data.get("key_concepts",[])
    if not topic or not lesson_title:
        return jsonify({"error": "topic and lesson_title are required"}), 400
    try:
        result = generate_notes(topic, lesson_title, video_id, key_concepts)
        return jsonify({"success": True, **result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
