import os
import psycopg2
from flask import Flask, render_template, redirect, url_for, request, flash, Blueprint
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm
from models import Users
from psycopg2 import sql



# init SQLAlchemy so we can use it later in our models
db = "dbname='flask_db' user='postgres' host='127.0.0.1' password = 'oyster44'"
#mysession = {"state" : "initializing","role" : "Not assingned", "id": 1 ,"age" : 202212}


app = Flask(__name__)
app.config['SECRET_KEY'] = 'fc089b9218301ad987914c53481bff04'


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='flask_db',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])

    return conn

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    schema = 'users'
    id = 'userid'

    user_sql = sql.SQL("""
    SELECT * FROM {}
    WHERE {} = %s
    """).format(sql.Identifier(schema),  sql.Identifier(id))

    cur.execute(user_sql, (int(user_id),))
    if cur.rowcount > 0:

        return Users(cur.fetchone())
    else:
        return None
    

def get_user_by_user_name(user_name):
    conn = get_db_connection()
    cur = conn.cursor()
    sql = """
    SELECT * FROM Users
    WHERE username = %s
    """
    cur.execute(sql, (user_name,))
    user = Users(cur.fetchone()) if cur.rowcount > 0 else None
    return user


def get_home_by_user_name(user_name):
    conn = get_db_connection()
    cur = conn.cursor()
    sql = """
    SELECT u.username, s.stationname, temp.temperature, case when temp.temperature < 10 then \'godt\' else \'ikke\' end as "svar" 
        FROM users u
        LEFT JOIN stations s ON s.stationID = u.favoritestation
        JOIN ( SELECT m.temperature, m.stationID, m.measurementdate
        FROM measurements m
        WHERE (EXTRACT(month FROM m.measurementdate), EXTRACT(day FROM m.measurementdate)) = (EXTRACT(month FROM CURRENT_DATE), EXTRACT(day FROM CURRENT_DATE))
        ) AS temp ON u.favoritestation = temp.stationID
        WHERE u.username = %s 
    """
    cur.execute(sql, (user_name,))
    user = Users(cur.fetchone()) if cur.rowcount > 0 else None
    print(user)
    return user


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    form = LoginForm()
    user = get_home_by_user_name(current_user.user_name)
    return render_template('home.html', users=user)


def home():
    return render_template('home.html')


@app.route("/", methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = get_user_by_user_name(form.user_name.data)
            if user and user[2] == form.password.data:
                login_user(user, remember=True)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
    return render_template('login.html', form=form)


