import os
from pathlib import Path
from sqlite3 import dbapi2 as sqlite3
from dotenv import load_dotenv
from quart import Quart

app = Quart(__name__)

app.config['MAX_CONTENT_LENGTH'] = 10000 * 1024 * 1024  # 10GB limit

app.config.update({
    "DATABASE": os.path.join(os.path.dirname(app.root_path), "database/files.db")
})

def _connect_db():
    engine = sqlite3.connect(app.config["DATABASE"])
    engine.row_factory = sqlite3.Row
    return engine

def init_db():
    db = _connect_db()
    with open(app.root_path + "/models/files/schema.sql", mode="r") as file_:
        db.cursor().executescript(file_.read())
    db.commit()
    
# Register blueprints
from src.controllers.file_controller import file_bp
app.register_blueprint(file_bp, url_prefix='/api')