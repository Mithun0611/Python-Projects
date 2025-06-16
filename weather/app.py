from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from db import db, User, Search
from weather_api import get_forecast
import plotly.graph_objs as go
import json
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db.init_app(app)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register.html', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        uname = request.form['username']
        pwd = request.form['password']
        if User.query.filter_by(username=uname).first():
            return "User already exists"
        user = User(username=uname, password=pwd)
        db.session.add(user)
        db.session.commit()
        return redirect('/login.html')
    return render_template("register.html")

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        uname = request.form['username']
        pwd = request.form['password']
        user = User.query.filter_by(username=uname, password=pwd).first()
        if user:
            session['user_id'] = user.id
            return redirect('/dashboard.html')
        return "Invalid credentials"
    return render_template("login.html")

@app.route('/dashboard.html', methods=['GET', 'POST'])
def dashboard():
    forecast_data = None
    plot_url = ""
    if 'user_id' not in session:
        return redirect('/login.html')

    if request.method == 'POST':
        city = request.form['city']
        forecast_data = get_forecast(city)
        if forecast_data:
            user = User.query.get(session['user_id'])
            result = json.dumps(forecast_data)
            search = Search(city=city, result=result, user=user)
            db.session.add(search)
            db.session.commit()

            # Plot
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=forecast_data['times'], y=forecast_data['temps'], mode='lines+markers', name='Temp'))
            fig.update_layout(title=f"5-Day Forecast for {city}", xaxis_title="Time", yaxis_title="Temp (°C)")
            plot_url = fig.to_html(full_html=False)

    return render_template('dashboard.html', plot_url=plot_url)

@app.route('/history.html')
def history():
    if 'user_id' not in session:
        return redirect('/login.html')
    user_searches = Search.query.filter_by(user_id=session['user_id']).order_by(Search.timestamp.desc()).all()
    return render_template("history.html", searches=user_searches)

@app.route('/forgot.html', methods=['GET', 'POST'])
def forgot():
    if request.method == "POST":
        uname = request.form['username']
        user = User.query.filter_by(username=uname).first()
        if user:
            otp = str(random.randint(100000, 999999))
            session['otp'] = otp
            session['reset_user_id'] = user.id

            msg = Message("OTP for Password Reset", sender='your-email@gmail.com', recipients=[user.email])
            msg.body = f"Your OTP is: {otp}"
            mail.send(msg)

            return redirect('/verify_otp.html')
        return "User not found"
    return render_template("forgot.html")


@app.route('/reset.html', methods=['GET', 'POST'])
def reset():
    if 'reset_user_id' not in session:
        return redirect('/forgot.html')
    if request.method == "POST":
        new_pwd = request.form['new_password']
        user = User.query.get(session['reset_user_id'])
        user.password = new_pwd
        db.session.commit()
        session.pop('reset_user_id', None)
        return redirect('/login.html')
    return render_template("reset.html")

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'fhms xqgl reai oxuu'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

@app.route('/verify_otp.html', methods=['GET', 'POST'])
def verify_otp():
    if request.method == "POST":
        user_otp = request.form['otp']
        if session.get('otp') == user_otp:
            session.pop('otp', None)
            return redirect('/reset.html')
        else:
            return "Invalid OTP"
    return render_template("verify_otp.html")


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
