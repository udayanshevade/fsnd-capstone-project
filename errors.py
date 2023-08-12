from flask import jsonify
from auth import AuthError


# Error Handling
def app_error_handling(app):
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


    @app.errorhandler(AuthError)
    def handle_auth_error(self, error: AuthError):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error['description']
        }), error.status_code,
