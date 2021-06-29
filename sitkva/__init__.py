import os
from dotenv import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate




app = Flask(__name__)



load_dotenv()

DB_USER = os.environ.get("LOCAL_DB_USERNAME")
DB_USER_PASS = os.environ.get("LOCAL_DB_PASSWORD")
LOCAL_SERVER_HOST = os.environ.get("LOCAL_SERVER_HOST")
LOCAL_SERVER_PORT = os.environ.get("LOCAL_SERVER_PORT")
LOCAL_SERVER_DB = os.environ.get("LOCAL_SERVER_DB")




app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{DB_USER}:{DB_USER_PASS}@{LOCAL_SERVER_HOST}:{LOCAL_SERVER_PORT}/{LOCAL_SERVER_DB}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)



from sitkva import routes
