from flask import Flask
from .models import db, NoAdmissions
from .config import Config
from .pcc_api import make_request

app = Flask(__name__)
app.config.from_object(Config)


with app.app_context():
    db.init_app(app)
    db.create_all()

from . import routes

