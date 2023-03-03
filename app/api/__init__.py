from flask import Blueprint, jsonify

bp = Blueprint("apiv1", __name__)

from app.api import post_routes, profile_routes


@bp.errorhandler(404)
def page_not_found(error):
    # app.logger.error('404', exc_info=sys.exc_info())
    return jsonify(message="Page Not Found", error=str(error)), 404


@bp.errorhandler(500)
def internal_error(error):
    # app.logger.error('Unhandled exception', exc_info=sys.exc_info())
    return jsonify(message="Something went wrong on server.", error=str(error)), 500
