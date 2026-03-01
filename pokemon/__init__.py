# postgresql://pokemon_db_natthawutnin_user:NA98kilRq7OtIY3COqfVQoJ4LU3jed4v@dpg-d69sc2mr433s73d8cttg-a.singapore-postgres.render.com/pokemon_db_natthawutnin

import os
from flask import Flask, app
from pokemon.extensions import db, login_manager, bcrypt
import pokemon.models as models
from pokemon.core.routes import core as core_bp
from pokemon.users.routes import users_bp
from pokemon.pokemon.routes import pokemon_bp

def create_app():
    app = Flask(__name__)

    # ✅ ใช้ของ Render ถ้ามี ไม่งั้นใช้ sqlite local
    database_url = None

    if database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(pokemon_bp, url_prefix='/')
    app.register_blueprint(core_bp, url_prefix='/')
    app.register_blueprint(users_bp, url_prefix='/users')

    return app