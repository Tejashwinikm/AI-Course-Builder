"""
AI Course Builder — Flask Backend
==================================
Stack: Python + Flask + LangChain + SQLite
"""
import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from routes.course_routes import course_bp
from routes.quiz_routes import quiz_bp
from routes.video_routes import video_bp
from routes.notes_routes import notes_bp
from routes.progress_routes import progress_bp
from routes.mentor_routes import mentor_bp
from services.progress_service import init_db


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod")

    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000"]}})

    init_db()

    app.register_blueprint(course_bp,   url_prefix="/api/course")
    app.register_blueprint(quiz_bp,     url_prefix="/api/quiz")
    app.register_blueprint(video_bp,    url_prefix="/api/video")
    app.register_blueprint(notes_bp,    url_prefix="/api/notes")
    app.register_blueprint(progress_bp, url_prefix="/api/progress")
    app.register_blueprint(mentor_bp,   url_prefix="/api/mentor")

    @app.route("/api/health")
    def health():
        mode = "mock" if os.environ.get("USE_MOCK", "true").lower() == "true" else "live"
        return {"status": "ok", "mode": mode}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
