from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
import requests
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hotel_secret_key_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# МӘЛІМЕТТЕР ҚОРЫНЫҢ ҚҰРЫЛЫМЫ
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='client') # admin, manager, employee, moderator, client

# РӨЛДЕРГЕ БАЙЛАНЫСТЫ ҚҰҚЫҚТАРДЫ ШЕКТЕУ ДЕКОРАТОРЫ
def role_required(roles_list):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles_list:
                return "Сізде бұл бетті көруге құқығыңыз жоқ!", 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/')
def index():
    # АРІ ИНТЕГРАЦИЯСЫ: Валюта курсын алу
    usd_rate = 450.0
    try:
        response = requests.get("https://open.er-api.com/v6/latest/USD")
        if response.status_code == 200:
            usd_rate = response.json()["rates"]["KZT"]
    except:
        pass
    return f"Қонақүй жүйесіне қош келдіңіз! Ағымдағы USD курсы: {usd_rate} KZT"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
