from flask import Flask
from flask_pymongo import PyMongo
app = Flask(__name__, template_folder='templates',static_folder='static')
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydb"
app.secret_key = 'bhdjhb124kjbdfjkbldlkd'
mongo = PyMongo(app)


from main import routes