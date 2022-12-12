from flask import Flask, render_template, flash, redirect, request, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
import requests
import random
import json
import random
from urllib.request import urlopen
from datetime import datetime, timedelta


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['DEBUG'] = True

app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap(app)

weatherApiKey = '0779b698eafe3111d7cd9c4a487dd8e6'
# app.config['GOOGLEMAPS_KEY'] = 'AIzaSyDHHAdcVxD1s6y6CrUHN4dnaaE0Mxgv2Sg'
GoogleMaps(app, key="AIzaSyDHHAdcVxD1s6y6CrUHN4dnaaE0Mxgv2Sg")


class City(FlaskForm):
  city_name = StringField('City Name', validators=[DataRequired()])


# def changeCity(city):
#   global cityName
#   cityName = city

cities = []

#set this to get the # of weeks for forecast
weeks = 2


def getWeekdays(weekCount):
  #list of days
  weekdays = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday",
    "Sunday"
  ]
  #get the current day
  date = datetime.now()
  day = date.weekday()
  #start new list from current day until end of weekday list
  week = weekdays[day:7]
  #extend it from the beggining until the current day
  week.extend(weekdays[0:day])
  #extends the list based on the weeks arguement, 2 will return days for 2 weeks
  week *= weekCount
  # weekdays = start
  return week


weekdays = getWeekdays(weeks)


def getWeek(weekCount):
  week = []
  #get the current day
  currentDay = datetime.now()
  # go in the range for weeks
  days = 7 * weekCount
  for i in range(0, days):
    #convert to the format currently month/day ex. 11/27
    formattedDay = currentDay.strftime("%m/%d")
    #add it to the list
    week.append(formattedDay)
    #go to the next day
    currentDay += timedelta(1)
  return week


week = getWeek(weeks)

days = 7 * weeks


def getCurrentLocation():
  try:
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    data = json.load(response)
    return data["city"]
  except:
    print("error")


def getCityPicture(name):
  try:
    url = "https://pixabay.com/api/?key=23607434-f985c753fecbdf81bcf90a5d6&q=" + name + "&image_type=photo&per_page=5"
    r = requests.get(url)
    data = r.json()
    img = random.randrange(1, 5)
    return data["hits"][img]['imageURL']
  except:
    print("error")


cityName = getCurrentLocation()


@app.route('/', methods=('GET', 'POST'))
def main():
  global cityName
  cityName = getCurrentLocation()
  form = City()
  url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&cnt=14&appid={}".format(
    cityName, weatherApiKey)

  try:
    r = requests.get(url)
    data = r.json()      
  except:
    print('please try again')
    data = 'error'

  if form.validate_on_submit():
    cityName = form.city_name.data
    # changeCity(city)
    return redirect('/weather')
  return render_template('home.html',
                         form=form,
                         current=getCurrentLocation(),
                         data=data)


@app.route('/random', methods=('GET', 'POST'))
def randCity():
  global cityName
  randCode = [48322,11419,55082,18015,60120]
  randZip = randCode[random.randint(0,4)]
  
  url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(randZip, weatherApiKey)
  img = "https://source.unsplash.com/random/1600x900/?" + cityName
  form = City()
  try:
    r = requests.get(url)
    data = r.json()
    
      
  except:
    print('please try again')
    data = 'error'
  if form.validate_on_submit():
    cityName = form.city_name.data
    # changeCity(city)
    return redirect('/weather')
  return render_template('randWeather.html',
                         form=form,
                         current=getCurrentLocation(),
                         img=img,
                         data=data)
  
@app.route('/weather', methods=('GET', 'POST'))
def displayWeather():
  # city = cities[0]
  img = "https://source.unsplash.com/random/1600x900/?" + cityName
  url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&cnt=14&appid={}".format(
    cityName, weatherApiKey)
  form = City()
  try:
    r = requests.get(url)
    data = r.json()
  except:
    print('please try again')
    data = 'error'

  return render_template('weather.html', data=data, img=img, form=form)


@app.route('/forecast', methods=('GET', 'POST'))
def displayForeCast():
  img = "https://source.unsplash.com/random/1600x900/?" + cityName
  url = "https://pro.openweathermap.org/data/2.5/forecast/climate?q={}&units=imperial&cnt={}&appid={}".format(
    cityName, days, weatherApiKey)
  form = City()
  try:
    r = requests.get(url)
    data = r.json()
  except:
    print('please try again')
    data = 'error'

  return render_template('forecast.html',
                         data=data,
                         img=img,
                         form=form,
                         week=week,
                         weekdays=weekdays)


@app.route("/map")
def mapview():
  # creating a map in the view
  mymap = Map(identifier="view-side",
              lat=37.4419,
              lng=-122.1419,
              markers=[(37.4419, -122.1419)])
  sndmap = Map(identifier="sndmap",
               lat=37.4419,
               lng=-122.1419,
               markers=[{
                 'icon':
                 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                 'lat': 37.4419,
                 'lng': -122.1419,
                 'infobox': "<b>Hello World</b>"
               }, {
                 'icon':
                 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                 'lat': 37.4300,
                 'lng': -122.1400,
                 'infobox': "<b>Hello World from other place</b>"
               }])
  return render_template('example.html', mymap=mymap, sndmap=sndmap)


app.run(host='0.0.0.0', port=8080)
