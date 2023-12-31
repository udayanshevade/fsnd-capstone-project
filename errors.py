from flask import jsonify
from auth import AuthError


# Error Handling
def app_error_handling(app):
    @app.errorhandler(400)
    def malformed(self):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "malformed"
        }), 400

    @app.errorhandler(422)
    def unprocessable(self):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def unreachable(self):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'unreachable'
        }), 404

    @app.errorhandler(500)
    def internal_error(self):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal_server_error'
        })

    @app.errorhandler(AuthError)
    def handle_auth_error(error: AuthError):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error['description']
        }), error.status_code,
