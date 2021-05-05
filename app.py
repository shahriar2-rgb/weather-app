import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecret'

db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={ city }&units=metric&appid=4c65edd7a717e23ee614acd543adccec'
    r = requests.get(url).json()
    return r

@app.route('/')
def index_get():
    cities = City.query.all()

    weather_data = []

    for city in cities:

        r = get_weather_data(city.name)
        print(r)

        weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'feels_like': r['main']['feels_like'],
            'High': r['main']['temp_max'],
            'pressure': r['main']['pressure'],
            'Low': r['main']['temp_min'],
            'description': r['weather'][0]['description'],
            'humidity': r['main']['humidity'],
            'wind_speed': r['wind']['speed'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(weather)
        new =weather_data[-1]
        #


    return render_template('index.html', weather_data=weather_data, new_data=new)

@app.route('/', methods=['POST'])
def index_post():
    err_msg = ''
    new_city = request.form.get('city')
        
    if new_city:
        existing_city = City.query.filter_by(name=new_city).first()

        if not existing_city:
            new_city_data = get_weather_data(new_city)

            if new_city_data['cod'] == 200:
                new_city_obj = City(name=new_city)

                db.session.add(new_city_obj)
                db.session.commit()
            else:
                err_msg = 'City does not exist in the world!'
                return render_template("404.html")
        else:
            r1 = get_weather_data(existing_city.name)
            print(r1)
            k=[]
            weather = {
                'city': existing_city.name,
                'temperature': r1['main']['temp'],
                'feels_like': r1['main']['feels_like'],
                'High': r1['main']['temp_max'],
                'pressure': r1['main']['pressure'],
                'Low': r1['main']['temp_min'],
                'description': r1['weather'][0]['description'],
                'humidity': r1['main']['humidity'],
                'wind_speed': r1['wind']['speed'],
                'icon': r1['weather'][0]['icon'],
            }
            k.append(weather)
            return render_template('one_city.html', weather=k[0])
            



    if err_msg:
        flash(err_msg, 'error')
    else:
        flash('City added succesfully!')

    return redirect(url_for('index_get'))

@app.route('/delete/<name>')
def delete_city(name):
    city = City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()

    flash(f'Successfully deleted { city.name }', 'success')
    return redirect(url_for('index_get'))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')