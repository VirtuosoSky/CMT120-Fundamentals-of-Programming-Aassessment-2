from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '<1d42cfac719bdd03311cb938e1336597c919b582692fe45d>'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c21100496:Jamesbond0621.@csmysql.cs.cf.ac.uk:3306/c21100496_flask_assessment'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


from blog import routes