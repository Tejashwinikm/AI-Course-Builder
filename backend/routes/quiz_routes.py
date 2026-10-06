from flask import Blueprint, request, jsonify
from services.ai_service import generate_quiz

quiz_bp = Blueprint("quiz", __name__)

@quiz_bp.route("/generate", methods=["POST"])
def generate():
    data = request.get_json() or {}
    topic, module_title = data.get("topic",""), data.get("module_title","")
    lesson_title, key_concepts = data.get("lesson_title",""), data.get("key_concepts",[])
    if not topic or not lesson_title:
        return jsonify({"error": "topic and lesson_title are required"}), 400
    try:
        return jsonify({"success": True, "quiz": generate_quiz(topic, module_title, lesson_title, key_concepts)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
