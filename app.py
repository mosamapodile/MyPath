"""
Main Application Entry Point for MyPath.
Registers routes, static files, and environment configurations.
"""

import os
from flask import Flask, render_template, jsonify
from routes.api import api_bp

def create_app() -> Flask:
    app = Flask(__name__)
    
    # Load configuration settings
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "mypath-secret-key-dev")
    app.config["JSON_SORT_KEYS"] = False

    # Register API Blueprint
    app.register_blueprint(api_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/health")
    def health_check():
        return {"status": "healthy", "service": "MyPath API"}, 200

    # Ensure unhandled server errors return JSON instead of default HTML pages
    @app.errorhandler(500)
    def handle_500_error(e):
        return jsonify({
            "status": "error",
            "message": "Internal Server Error",
            "details": str(e)
        }), 500

    @app.errorhandler(404)
    def handle_404_error(e):
        return jsonify({
            "status": "error",
            "message": "Endpoint not found"
        }), 404

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_ENV") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)