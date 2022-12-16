# Authors: Marcos Carrero, Gerardo Solis, Anisha Jadhav, Joseph Arredondo
# Abstract:
# Fall 2022

#Work disrubution:

#Joseph Arredondo:
#Functions: getWeekdways, getWeek, getCurrentLocation,displayForecast
#File: forecast.html

# Marcos Carrero:
#Functions: main, displayWeather, coordsRoute, displayCoordsForeCast, GoogleMapsAPI
#File: home.html, mapWeather.html, weather.html searchBtns.html, nav.html

#Gerardo Solis:
#Functions: randCity
#File: randWether.html

#Anisha Jadhav:
#Functions: login, logout, signup
#File: login.html, signupp.html


from flask import Flask, render_template, flash, redirect, request, jsonify, session, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm

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

#Flask Form for city search
class City(FlaskForm):
  city_name = StringField('City Name', validators=[DataRequired()])

#flask Form for Map/coords search
class Coord(FlaskForm):
  lat = StringField("Lat", validators=[DataRequired()])
  lon = StringField("Lon", validators=[DataRequired()])


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

# get week
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

# Get user location
def getCurrentLocation():
  try:
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    data = json.load(response)
    return data["city"]
  except:
    print("error")

#random city background picture
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
lat = 37.338207;
lon = -121.886330;

# Home Page
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

# Random city
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
  cityName = data["name"]
  if form.validate_on_submit():
    cityName = form.city_name.data
    # changeCity(city)
    return redirect('/weather')
  return render_template('randWeather.html',
                         form=form,
                         current=getCurrentLocation(),
                         img=img,
                         data=data)
  
# Display weather for search result
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

# Displays forecast for selected city
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

# Displays forecast for city searched by coords
@app.route('/coordsForecast', methods=('GET', 'POST'))
def displayCoordsForeCast():
  img = "https://source.unsplash.com/random/1600x900/?" + cityName
  url = "https://pro.openweathermap.org/data/2.5/forecast/climate?lat={}&lon={}&units=imperial&appid={}".format( lat, lon, weatherApiKey)
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

# Search by Google Maps Route
@app.route('/map', methods=('GET', 'POST'))
def coordsRoute():
  global cityName
  global lat
  global lon
  cityName = getCurrentLocation()
  form = Coord();
  url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=imperial&appid={}".format( lat, lon, weatherApiKey)

  try:
    r = requests.get(url)
    data = r.json()      
  except:
    print('please try again')
    data = 'error'

  if form.validate_on_submit():
    lat = form.lat.data
    lon = form.lon.data
    # changeCity(city)
    return redirect('/map')
  return render_template('mapWeather.html',
                         form=form,
                         current=getCurrentLocation(),
                         data=data, lat=lat,lon=lon)

# Login page
@app.route('/login', methods=["GET","POST"])
def login():
 
  if request.method == "POST":
      email = request.form.get("email")
      password = request.form.get("password")
      print(email,password)
      conn = mysql.connect()
      cur = conn.cursor()
      cur.execute("select * from authentication where email=%s;",[email])
      data = cur.fetchone()
      cur.close()
      conn.close()
      if data != None:
          if data[4] == password:
              session["auth_id"] = data[0]
              session["first_name"] = data[1]
              session["last_name"] = data[2]
              session["email"] = data[3]
              return redirect(url_for("main"))
          else:
              session["error"] = "password doesn't match."
              return redirect(url_for("login"))

      else:
          session["error"] = "user not exist."
          return redirect(url_for("login"))
  else:
    return render_template("login.html")

# SignUp page
@app.route("/signup",methods=["GET","POST"])
def signup():
  if request.method == "POST":
      first_name = request.form.get("first_name")
      last_name = request.form.get("last_name")
      email = request.form.get("email")
      password = request.form.get("password")
      conn = mysql.connect()
      cur = conn.cursor()
      cur.execute(""" select * from authentication where email=%s ; """,[email])
      data = cur.fetchone()
      if data == None:
          cur.execute(''' insert into authentication (first_name,last_name,email,password) values(%s,%s,%s,%s);''',[first_name,last_name,email,password])
          conn.commit()
          cur.close()
          conn.close()
          return redirect("/home")
      else:
          session["error"] = "This Email Address Is Already Exist"
          return redirect("/signup")
  else:
      user_name = session.get("user_name")

      error = ""
      if session.get("error"):
          error = session.get("error")
          session.pop("error", None)

      return render_template("signupp.html",user_name=user_name,error=error)

# Logout route
@app.route("/logout",methods=["GET","POST"])
def logout():
  session.pop("first_name", None)
  session.pop("last_name", None)
  session.pop("email", None)
  session.pop("auth_id", None)
  return redirect(url_for("login"))


app.run(host='0.0.0.0', port=8080)
