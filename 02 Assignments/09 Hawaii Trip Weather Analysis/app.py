from flask import Flask, jsonify
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import numpy as np
import pandas as pd

engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})
# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes

# for Home page
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Trip API:<br/>"
        f"Here are routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/'start date'<br>"
		f"/api/v1.0/roundtrip/'start date'/'end date'"
    )

# for Precipitation page
@app.route("/api/v1.0/precipitation")
def prcp():
    # Latest Date in the data set provided
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_date = "".join([x for x in latest_date])

    # Set date of a year ago
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    precp_year_ago = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= year_ago).\
    filter(Measurement.prcp != "None").\
    group_by(Measurement.date).all()

    # Make dict
    web_prcp = []
    for prcp in precp_year_ago:
        prcp_dict = {}
        prcp_dict["date"] = prcp[0]
        prcp_dict["prcp"] = prcp[1]
        web_prcp.append(prcp_dict)
    return jsonify(web_prcp)

# for Stations page
@app.route("/api/v1.0/stations")
def stat():
    results = session.query(Station.station, Station.name).all()
    
    return jsonify(results)

# for Temperature Observation Station page
@app.route("/api/v1.0/tobs")
def tobs():
    # Set date of a year ago
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    tobs_year_ago = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= year_ago).\
    filter(Measurement.prcp != "None").\
    group_by(Measurement.date).all()

    # Make dict
    web_tobs = []
    for tob in tobs_year_ago:
        tobs_dict = {}
        tobs_dict["date"] = tob[0]
        tobs_dict["tobs"] = tob[1]
        web_tobs.append(tobs_dict)
    return jsonify(web_tobs)

# for Start date page
@app.route("/api/v1.0/<start_date>")
def findstart(start_date):
    #Return the avg, max, min, temp over a specific time period
    results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    # 404 error build
    earliest_date = session.query(Measurement.date).order_by(Measurement.date).first()
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    earliest_date = "".join([x for x in earliest_date])
    latest_date = "".join([x for x in latest_date])

    if earliest_date < start_date and start_date < latest_date:
        data_list = []
        for result in results:
            row = {}
            row["Start Date"] = start_date
            row["Average Temperature"] = float(result[0])
            row["Highest Temperature"] = float(result[1])
            row["Lowest Temperature"] = float(result[2])
            data_list.append(row)
        return jsonify(data_list)
    return jsonify({"error": "Date not found, please use '%Y-%M-%D' formate or choose a date within range"}), 404    


# for Start & End date page
@app.route("/api/v1.0/roundtrip/<start_date>/<end_date>")
def roundtrip(start_date, end_date):
    #Return the avg, max, min, temp over a specific time period
    results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

# 404 error build
    earliest_date = session.query(Measurement.date).order_by(Measurement.date).first()
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    earliest_date = "".join([x for x in earliest_date])
    latest_date = "".join([x for x in latest_date])

    if earliest_date < start_date and start_date < latest_date and earliest_date < end_date and end_date < latest_date:
        data_list = []
        for result in results:
            row = {}
            row["Start Date"] = start_date
            row["End Date"] = end_date
            row["Average Temperature"] = float(result[0])
            row["Highest Temperature"] = float(result[1])
            row["Lowest Temperature"] = float(result[2])
            data_list.append(row)
        return jsonify(data_list)
    return jsonify({"error": "Date not found, please use '%Y-%M-%D' formate or choose a date within range"}), 404


if __name__ == "__main__":
    app.run(debug=True)

