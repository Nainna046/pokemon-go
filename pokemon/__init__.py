# postgresql://pokemon_db_natthawutnin_user:NA98kilRq7OtIY3COqfVQoJ4LU3jed4v@dpg-d69sc2mr433s73d8cttg-a.singapore-postgres.render.com/pokemon_db_natthawutnin

import os
from flask import Flask, app
from pokemon.extensions import db, login_manager, bcrypt
import pokemon.models as models
from pokemon.core.routes import core as core_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(core_bp, url_prefix='/')
    
    return app