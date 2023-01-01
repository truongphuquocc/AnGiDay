from flask import Flask
from config import Config
app = Flask(__name__)
#app.config['SECRET_KEY'] = 'hard-secret-key'
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.app_context().push()

from flask_login import LoginManager
login = LoginManager(app)
login.login_view = 'login'

from app import routes
from app import models
