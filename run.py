import os
import config
from app import create_app
from install.settings import register_general_settings


config_class = (
    config.DevelopmentConfig
    if os.environ.get("FLASK_ENV") == "development"
    else config.ProductionConfig
)
app = create_app(config_class)

# check here if the blog needs installation before start responsing to requests
# @app.before_first_request
# def before_first_request():
#     app.logger.info("we are checking if everything is good and the app is installed.")

#     ## check
#     register_general_settings()
