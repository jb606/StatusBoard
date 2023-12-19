from flask import Flask, flash
from flask_sqlalchemy import SQLAlchemy
from flask_oidc import OpenIDConnect
from werkzeug.exceptions import HTTPException
from .errors import handle_exception

# Setup the database handle
db = SQLAlchemy()

# Database Settings
DB_NAME = "statusboard.db"


# Create something to store the OpenID object
oidc = OpenIDConnect()





def create_app():
    app = Flask(__name__)
    app.config.update({
    'SQLALCHEMY_DATABASE_URI': f'sqlite:///{DB_NAME}',
    'SECRET_KEY': 'ksjdfasiuv9f099fu980vsds9fdsdf',
    'SESSION_TYPE': 'filesystem'
    })
    db.init_app(app)
    
    
    from .userviews import userviews
    from .groupviews import groupviews
    from .statusviews import statusviews
    from .errors import handle_exception
    app.register_blueprint(userviews, url_prefix='/')
    app.register_blueprint(statusviews, url_prefix='/')
    app.register_blueprint(groupviews, url_prefix='/')
    app.register_error_handler(500, handle_exception)
    
    app.config.update({
        'OIDC_CLIENT_SECRETS': 'client_secrets.json',
        'OIDC_ID_TOKEN_COOKIE_SECURE': False,
        'OIDC_COOKIE_SECURE': False,
        'OIDC_USER_INFO_ENABLED': True,
        'OIDC_OPENID_REALM': 'A-LAN',
        'OIDC_SCOPES': ['openid', 'email', 'profile', 'groups'],
        'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post'
    })
    app.config.from_prefixed_env(prefix='SB_')
    

    oidc = OpenIDConnect(app)
    with app.app_context():
            db.create_all()

    return app
