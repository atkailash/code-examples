#!/usr/bin/env python3
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from models import CoordinateForm

class Config(object):
    SECRET_KEY = "NOTSOSECRET" # Can also be env variable or file
    DEBUG = True

app = Flask(__name__)
app.config.from_object(Config)
Bootstrap(app)
                
@app.route("/", methods=["GET", "POST"])
def main_page():
    form = CoordinateForm(request.form)
    
    if not form.validate_on_submit():
        print("Not validated or not a post")
        print(f"Method: {request.method}")
        return render_template("index.jinja2", form=form)
    if request.method == "POST":
        print("Ok submit")
        return "Ok submit!"
    else:
        print("I dunno")

@app.route("/receive")
def receive_input(lat, long):
    try:
        lat = float(lat)
        long = float(long)
        if lat not in range(-90,91):
            raise ValueError(f"Latitude {lat} is out of bounds (not between -90 and 90)")
        elif long not in range(-180,181):
            raise ValueError(f"Longtitude {long} is out of bounds (not between -180 and 180)")
        else:
            image_name = GetImageURL(lat, long)
            return(200, image_name)
    except ValueError as ve:
        print(f"Value Error: {ve}")
        return render_template("value_error.html"), 501

#@app.errorhandler(501)
#def not_implemented(error):

if __name__ == "__main__":
    app.run()