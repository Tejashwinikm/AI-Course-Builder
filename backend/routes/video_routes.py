from flask import Blueprint, request, jsonify
from services.youtube_service import search_videos

video_bp = Blueprint("video", __name__)

@video_bp.route("/search")
def search():
    query = request.args.get("q", "").strip()
    n = int(request.args.get("n", 3))
    if not query:
        return jsonify({"error": "q is required"}), 400
    try:
        return jsonify({"success": True, "videos": search_videos(query, n)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
