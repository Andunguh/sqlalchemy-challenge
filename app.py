import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base, name_for_collection_relationship
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask,jsonify



##########################################################
# Database setup

##########################################################
engine = create_engine("sqlite:///hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (f"Welcome to my 'Home' page!<br/>"
           f"&emsp;Available Routes:<br/>"
           f"&emsp;&emsp;1. /api/v1.0/precipitation<br/>"                  
           f"&emsp;&emsp;2. /api/v1.0/stations<br/>"
           f"&emsp;&emsp;3. /api/v1.0/tobs<br/>"
           f"&emsp;&emsp;4. /api/v1.0/start<br/>"
           f"&emsp;&emsp;5. /api/v1.0/start/end<br/>")

# Define what to do when a user hits the /api/v1.0/precipitation route

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    MaxDate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    MaxDate = MaxDate[0]
    MaxDay = int(MaxDate[-2:])
    MaxYear= int(MaxDate[:4])
    MaxMonth = int(MaxDate[5:7])
    previous_year = dt.date(MaxYear,MaxMonth,MaxDay)-dt.timedelta(days=365)

#Query all precipitation data. 
    prec_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= previous_year).order_by(Measurement.date).all()

    session.close()

 # Create a dictionary from the row data and append to a list of all_precipitation
    all_precipitation = []
    for date,prcp in prec_query:
        prec_dict = {}
        prec_dict[date] = prcp
        all_precipitation.append(prec_dict)

    return jsonify(all_precipitation)

# Define what to do when a user hits the /api/v1.0/stations route

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    station_query = session.query(Station.id, Station.station, Station.name).\
    all()

    session.close()

# Create a dictionary from the row data and append to a list of all_precipitation
    all_stations = []
    for id, station, name in station_query:
        station_dict = {}
        station_dict[id] = [station, name]
        all_stations.append(station_dict)

    return jsonify(all_stations)

#  Define what to do when a user hits the api/v1.0/tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    MaxDate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    MaxDate = MaxDate[0]
    MaxDay = int(MaxDate[-2:])
    MaxYear= int(MaxDate[:4])
    MaxMonth = int(MaxDate[5:7])
    previous_year = dt.date(MaxYear,MaxMonth,MaxDay)-dt.timedelta(days=365)

    tobs_query = session.query(Station.name, Measurement.date, Measurement.tobs).\
    filter(Station.station == Measurement.station,Station.id == '7', Measurement.date >= previous_year).all()

    session.close()

# Create a dictionary from the row data and append to a list of all_precipitation
    all_tobs = []
    for date,name,tobs in tobs_query:
        tobs_dict = {}
        tobs_dict[name] = [date,tobs]
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

# Define what to do when a user hits the /api/v1.0/<start> route

@app.route("/api/v1.0/<start>")
def startdate(start = ""):

    session = Session(engine)

    selection = [func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)]
    start = dt.datetime.strptime(start,"%m%d%Y")
    results = session.query(*selection).filter(Measurement.date >= start).all()

    return jsonify(list(np.ravel(results)))

    session.close()

#  Define what to do when a user hits the /api/v1.0/<start>/<end> route
@app.route("/api/v1.0/<start>/<end>")
def start_and_end(start = "", end  = ""):

    session = Session(engine)

    selection = [func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)]
    start = dt.datetime.strptime(start,"%m%d%Y")
    end = dt.datetime.strptime(end,"%m%d%Y")
    results = session.query(*selection).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    return jsonify(list(np.ravel(results)))

    session.close()


if __name__ == "__main__":
    app.run(debug=True) 



    










