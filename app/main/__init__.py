from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

from app.main import routes

@bp.errorhandler(404)
def page_not_found(error):
    #app.logger.error('404', exc_info=sys.exc_info())
    return render_template('errors/404.html', error=error)

@bp.errorhandler(500)
def internal_error(error):
    #app.logger.error('Unhandled exception', exc_info=sys.exc_info())
    return render_template('errors/500.html', error=error)