#  import Flask
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

from flask import Flask, jsonify
import datetime as dt
from datetime import datetime


# Database setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()
Base = automap_base()
Base.prepare(engine, reflect=True)
measurement = Base.classes.measurement
station = Base.classes.station

# Create an app
app = Flask(__name__)


# Flask routes

@app.route("/")
def home():
    return (
        f"Welcome to the home page<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first() 
    recent_date = datetime.strptime(recent_date[0],"%Y-%m-%d")
    start_date = dt.date(recent_date.year - 1, recent_date.month, recent_date.day)
    sel = [measurement.date, measurement.prcp]
    results = session.query(*sel).\
    filter(measurement.date >= start_date).all()
    session.close()
    
    # Convert to dictionary
    results_list=[]
    for row in results:
        dict={}
        dict[row[0]]=row[1]
    results_list.append(dict)
    
    return jsonify(results_list)
        
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(station.name).all()
    session.close()
    results_list = []
    for name in results:
        results_list.append(name[0])
    
    return jsonify(results_list)
        
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)    
    active_id = 'USC00519281'
    recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first() 
    recent_date = datetime.strptime(recent_date[0],"%Y-%m-%d")
    start_date = dt.date(recent_date.year - 1, recent_date.month, recent_date.day)
    results = session.query(measurement.date,measurement.tobs).\
    filter((measurement.station == active_id) & (measurement.date >=start_date)).all()    
    session.close()
    
    list=[]
    for tobs in results:
        list.append(tobs[1])
    
    return jsonify(list)
    
@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    sel = [func.avg(measurement.tobs),func.min(measurement.tobs),func.max(measurement.tobs)]
    results = session.query(*sel).\
    filter(measurement.date >= start).all()
    session.close()
    
    dict={}
    dict["Avg Temp"]=results[0][0]
    dict["Min Temp"]=results[0][1]
    dict["Max Temp"]=results[0][2]
    
    return jsonify(dict)

@app.route("/api/v1.0/<start>/<end>")        
def startend(start,end):        
    session = Session(engine)    
    sel = [func.avg(measurement.tobs),func.min(measurement.tobs),func.max(measurement.tobs)]
    results = session.query(*sel).\
    filter((measurement.date >= start)&(measurement.date<end)).all()
    session.close()
    
    dict={}
    dict["Avg Temp"]=results[0][0]
    dict["Min Temp"]=results[0][1]
    dict["Max Temp"]=results[0][2]
    
    return jsonify(dict)
    
    
if __name__ == "__main__":
    app.run(debug=True)

