from flask import Blueprint, render_template, request, jsonify

error_bp = Blueprint('error_handlers', __name__)

def wants_json() -> bool:
    """Determine if client preferred JSON response."""
    return request.path.startswith('/api/') or request.accept_mimetypes.best == 'application/json'

@error_bp.app_errorhandler(400)
def bad_request(e):
    if wants_json():
        return jsonify({"error": "Bad Request", "message": str(e)}), 400
    return render_template('errors/400.html', error=str(e)), 400

@error_bp.app_errorhandler(404)
def not_found(e):
    if wants_json():
        return jsonify({"error": "Resource Not Found", "message": "The requested endpoint does not exist."}), 404
    return render_template('errors/404.html'), 404

@error_bp.app_errorhandler(500)
def server_error(e):
    if wants_json():
        return jsonify({"error": "Internal Server Error", "message": "An unexpected server error occurred."}), 500
    return render_template('errors/500.html'), 500
