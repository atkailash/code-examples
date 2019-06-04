#!/usr/bin/env python3
import random
from hashlib import md5
from string import ascii_letters, digits

import lrucache
from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_bootstrap.nav import BootstrapRenderer
from markupsafe import Markup
from models import CoordinateForm
from flask_nav import Nav
from flask_nav.elements import *
LRU = lrucache.LRUCache(3000)


class Config(object):
    SECRET_KEY = "NOTSOSECRET"  # Can also be env variable or file
    DEBUG = True


app = Flask(__name__)
app.config.from_object(Config)
Bootstrap(app)
nav = Nav()
nav.renderer(id=BootstrapRenderer, force=True)
@nav.navigation()
def the_bar():
    return Navbar("Mars Coords",
                  View("Enter Coordinates", "main_page"),
                  Subgroup("Show",
                            View("Counters", "show_counters"),
                            View("Show Everything", "show_all")
                            ),
                  Subgroup("Clear",
                            View("Clear Counters", "clear_counters"),
                            View("Clear Everything!", "clear_all")
                            )
                  )

nav.init_app(app)


@app.route("/", methods=["GET", "POST"])
def main_page():
    form = CoordinateForm(request.form)
    session["cleared_counters"] = False
    session["cleared_all"] = False
    if not form.validate_on_submit():
        return render_template("index.jinja2", form=form)
    elif form.validate_on_submit:
        lat = form.lat.data
        long = form.long.data
        session["lat"] = float(lat)
        session["long"] = float(long)
        return redirect(url_for("receive_input"))
    else:
        return 500


@app.route("/submit", methods=["GET"])
def receive_input():
    lat = session["lat"]
    long = session["long"]
    coords = str([lat, long])
    url = LRU.get(coords)
    if url == False:
        url = "https://marscoords.burks/" + GetURL(coords)
        LRU.add(coords, url)
        session["url"] = url
        return redirect(url_for("show_url"))
    elif url:
        return redirect(url_for("show_url"))
    else:
        return 500


@app.route("/show_url", methods=["GET"])
def show_url():
    return render_template("showurl.jinja2", url=session["url"])


@app.errorhandler(404)
def not_found(error):
    return "404 Not Found: These aren't the droids you're looking for."


@app.errorhandler(500)
def internal_server_Error(error):
    return error


def GetURL(coords):
    new_url = coords
    for x in range(30):
        new_url.join(random.choice(ascii_letters + digits))
    return md5(bytes(new_url, "UTF-8")).hexdigest()


@app.route("/counters", methods=["GET"])
def show_counters():
    if session["cleared_counters"] == True:
        flash("Cleared Counters", "success")
        session["cleared_counters"] = False
    return render_template("showcounters.jinja2", counter_stats=LRU.show_counters())


@app.route("/clear_counters", methods=["GET", "POST"])
def clear_counters():
    if request.method == "GET":
        flash("THIS WILL CLEAR COUNTERS!", "warning")
        return render_template("confirmcounters.jinja2")
    elif request.method == "POST":
        session["cleared_counters"] = True
        LRU.clear_counters()
        return redirect(url_for("show_counters"))
    else:
        return 501


@app.route("/clear_all", methods=["GET", "POST"])
def clear_all():
    if request.method == "GET":
        flash("THIS WILL REMOVE ALL DATA!", "danger")
        return render_template("confirmall.jinja2")
    elif request.method == "POST":
        session["cleared_all"] = True
        LRU.clear_all()
        return redirect(url_for("show_all"))
    else:
        return 501

@app.route("/show_all", methods=["GET"])
def show_all():
    cache_contents = LRU.dict_of_pairs
    cache_stats = LRU.show_counters()
    if session["cleared_all"] == True:
        flash("Cleared Counters and Cache", "success")
        session["cleared_all"] = False
    return render_template("showall.jinja2", counter_stats=cache_stats, cache_contents=cache_contents)


if __name__ == "__main__":
    app.run()
