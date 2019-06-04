#!/usr/bin/env python3
from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from models import CoordinateForm
from hashlib import md5
import random
import string
import lrucache

LRU = lrucache.LRUCache(3000)

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
    elif form.validate_on_submit:
        lat = form.lat.data
        long = form.long.data
        print(f"Lat Type: {type(lat)}, value: {lat}")
        print(f"Long Type: {type(long)}, value: {long}")
        session['lat'] = float(lat)
        session['long'] = float(long)
        return redirect(url_for("receive_input", lat, long))
    else:
        print("I dunno")

@app.route("/submit", methods=["POST"])
def receive_input(lat, long):
#    lat = session['lat']
#    long = session['long']
    coords = str([lat, long])
    url = LRU.get(coords)

        url = "https://marscoords.burks/" + GetURL(lat, long)

        return redirect(url_for("show_url"))
    except ValueError as ve:
        print(f"Value Error: {ve}")
        return render_template("value_error.html"), 501

@app.route("/show_url", methods=["GET"])
def show_url(lat, long):
    

@app.errorhandler(501)
def not_implemented(error):
    return "Oops"

def GetURL(lat, long):
    new_url = ""
    for x in range(30): new_url += random.choice(string.ascii_letters + string.digits)
    return new_url

if __name__ == "__main__":
    app.run()