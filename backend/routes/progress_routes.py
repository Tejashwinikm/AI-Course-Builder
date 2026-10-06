from flask import Blueprint, request, jsonify
from services.progress_service import create_course_record, mark_lesson_complete, get_course_progress, list_courses

progress_bp = Blueprint("progress", __name__)

@progress_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    course_id, course_title = data.get("course_id",""), data.get("course_title","")
    topic = data.get("topic","")
    total_lessons, total_quizzes = int(data.get("total_lessons",0)), int(data.get("total_quizzes",0))
    if not course_id or not course_title:
        return jsonify({"error": "course_id and course_title are required"}), 400
    try:
        create_course_record(course_id, course_title, topic, total_lessons, total_quizzes)
        return jsonify({"success": True, "progress": get_course_progress(course_id)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@progress_bp.route("/complete", methods=["POST"])
def complete():
    data = request.get_json() or {}
    course_id = data.get("course_id","")
    module_index, lesson_index = data.get("module_index"), data.get("lesson_index")
    lesson_type = data.get("lesson_type","video")
    quiz_score, quiz_total = data.get("quiz_score"), data.get("quiz_total")
    if not course_id or module_index is None or lesson_index is None:
        return jsonify({"error": "course_id, module_index, lesson_index required"}), 400
    try:
        progress = mark_lesson_complete(course_id, module_index, lesson_index, lesson_type, quiz_score, quiz_total)
        return jsonify({"success": True, "progress": progress})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@progress_bp.route("/<course_id>", methods=["GET"])
def get_progress(course_id):
    try:
        return jsonify({"success": True, "progress": get_course_progress(course_id)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@progress_bp.route("/", methods=["GET"])
def get_all():
    try:
        return jsonify({"success": True, "courses": list_courses()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
