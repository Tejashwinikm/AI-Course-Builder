from flask import Blueprint, request, jsonify
from services.course_service import build_course

course_bp = Blueprint("course", __name__)

@course_bp.route("/generate", methods=["POST"])
def generate():
    data        = request.get_json() or {}
    topic       = (data.get("topic") or "").strip()
    level       = data.get("level", "beginner")
    num_modules = max(2, min(5, int(data.get("num_modules", 4))))
    if not topic:
        return jsonify({"error": "topic is required"}), 400
    if level not in ("beginner", "intermediate", "advanced"):
        level = "beginner"
    try:
        course = build_course(topic=topic, level=level, num_modules=num_modules)
        return jsonify({"success": True, "course": course})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@course_bp.route("/status")
def status():
    return jsonify({"status": "ok"})
