from app.main import bp


@bp.app_errorhandler(404)
def not_found(code):
    return {"error": "Not Found", 'message': 'resource not found'}, 404


@bp.app_errorhandler(500)
def internal_server_error(code):
    return {"error": "Internal server error", 'message': 'Internal server error'}, 500

@bp.app_errorhandler(405)
def method_not_allowed(code):
    return {"error": "Method Not Allowed", 'message': 'The method is not allowed for the requested URL.'}, 405

def unauthorized(message):
    return {'error': 'unauthorized', 'message': message, "success": False}, 403