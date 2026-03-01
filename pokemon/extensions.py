from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'users.login'          # ⭐ บรรทัดสำคัญ
login_manager.login_message_category = 'warning'  # (optional แต่ดี)

bcrypt = Bcrypt()