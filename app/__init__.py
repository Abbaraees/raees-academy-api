from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

from config import Config


db = SQLAlchemy()
migrate = Migrate()



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)


    # register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.learn import bp as learn_bp
    app.register_blueprint(learn_bp, url_prefix='/learn')


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,OPTIONS')

        return response


    @app.route('/hello')
    def hello():
        return '<h1>Hello World</h1>'



    return app