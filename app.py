from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from models import User, create_tables, db
from forms import RegistrationForm, LoginForm
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route("/set_location", methods=['POST'])
def set_location():
    data = request.json
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    city = get_city_from_coordinates(latitude, longitude)
    weather_data = get_weather_data(city)
    air_quality_data = get_air_quality_data(city)

    return jsonify({"weather_data": weather_data, "air_quality_data": air_quality_data, "city": city})

def get_city_from_coordinates(latitude, longitude):
    nominatim_url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json"
    response = requests.get(nominatim_url)
    data = response.json()
    city = data.get("address", {}).get("city", "")
    return city

def get_weather_data(city):
    api_key = 'Api key'
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': api_key, 'units': 'metric'}

    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        weather_data = {
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'city': city
        }
        return weather_data

    return None

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Thank you for registering!', 'success')
        return redirect(url_for('login'))
    return render_template('registers.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/air_quality/<city>')
@login_required
def air_quality(city):
    air_quality_data = get_air_quality_data(city)
    return render_template('air_quality.html', air_quality_data=air_quality_data, city=city)

def get_air_quality_data(city):
    api_key = 'Api key'
    base_url = 'https://api.airvisual.com/v2/nearest_city?key=Api key'
    params = {'city': city, 'key': api_key}

    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        air_quality_data = {
            'aqi': data['data']['current']['pollution']['aqius'],
            'main_pollutant': data['data']['current']['pollution']['mainus']
        }
        return air_quality_data

    return None

if __name__ == "__main__":
    with app.app_context():
        create_tables()
    app.run(debug=True)



