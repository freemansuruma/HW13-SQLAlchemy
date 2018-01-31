import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite", echo=False)

Base = automap_base()
Base.prepare(engine, reflect=True)
stations = Base.classes.station_name
measurements = Base.classes.climate_measurements

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"- Precipitation<br/>"

        f"/api/v1.0/stations"
        f"- Stations<br/>"

        f"/api/v1.0/tobs"
        f"- Temperature<br/>"

        f"/api/v1.0/<start> and /api/v1.0/<start>/<end>"
        f"- minimum temperature, the average temperature, and the max temperature for a given start or start-end range<br/>"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date.today() - dt.timedelta(days=365)
    results = session.query(measurements.date,measurements.prcp).filter(measurements.date >= prev_year).all()

    prcp_list = []
    for result in results:
        row = {}
        row["date"] = result[0]
        row["prcp"] = float(result[1])
        prcp_list.append(row)

    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(stations.stations).all()

    station_list = list(np.ravel(results))

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    prev_year = dt.date.today() - dt.timedelta(days=365)
    results = session.query(measurements.date,measurements.tobs).filter(measurements.date >= prev_year).all()

    tobs_list = []
    for result in results:
        row = {}
        row["date"] = result[0]
        row["tobs"] = float(result[1])
        tobs_list.append(row)

    return jsonify(tobs_list)


if __name__ == '__main__':
    app.run()