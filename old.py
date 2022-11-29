# from flask import Flask, render_template, flash, redirect,request,jsonify
# # from flask_bootstrap import Bootstrap5
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired
# from datetime import datetime
# import requests
# import random

# app = Flask(  # Create a flask app
# 	__name__,
# 	template_folder='templates',  
# 	static_folder='static'  
# )
# if __name__ == "__main__":  
# 	app.run( 
# 		host='0.0.0.0', 
# 		port=random.randint(2000, 9000)  
# 	)
# app.config['SECRET_KEY'] = 'csumb-otter'
# # bootstrap = Bootstrap5(app)

# apiKey = '0779b698eafe3111d7cd9c4a487dd8e6'

# url = "https://pro.openweathermap.org/data/2.5/forecast/climate?q={}&units=imperial&cnt=14&appid={}".format('Seaside', apiKey)

# @app.route('/')
# def main():
#     try:
#         r = requests.get(url)
#         data = r.json()
#     except:
#         print('please try again')
#     return render_template('home.html', data=data)

# @app.route('/')  # '/' for the default page
# def home():
# 	return "Wow this is a basic output!"