
import datetime as dt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///data/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################
#Home page.
#List all routes that are available
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )
#/api/v1.0/precipitation
#Convert the query results to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create session 
    session = Session(engine)

        # Query all precipitation and date
    results = session.query(Measurement.date,Measurement.prcp).all()

    session.close()

    # Convert list of tuples into dictionary
    all_precepitation=[]
    for date,prcp in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        all_precepitation.append(precipitation_dict)

    return jsonify(all_precepitation)
#####################################################3

#/api/v1.0/stations
#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/Station")
def stations():
	#Return a list of all station names#
	# Query all stations
	results = session.query(Station.station).all()
    session.close()
  
	# Convert list of tuples into normal list
	#all_station = list(np.ravel(results))

	#Jsonify summary
	return jsonify(all_station)

    ####################################################
#/api/v1.0/tobs
#Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/tobs")
def tempartureobs():
    # Create  session 
    session = Session(engine)

# Calculate the date 1 year ago from the last data point in the database
    results_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    str_date=list(np.ravel(results_date))[0]
    latest_date=dt.datetime.strptime(str_date,"%Y-%m-%d")
    year_back=latest_date-dt.timedelta(days=366)
# Perform a query to retrieve the data and precipitation scores
    results=session.query(Measurement.date, Measurement.tobs).order_by(Measurement.date.desc()).\
            filter(Measurement.date>=year_back).all()
    session.close()
    all_temperature=[]
    for tobs,date in results:
        tobs_dict={}
        tobs_dict['date']=date
        tobs_dict['tobs']=tobs
        all_temperature.append(tobs_dict)
    return jsonify(all_temperature)

############################################################################################3
#/api/v1.0/<start> and /api/v1.0/<start>/<end>
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start>")
def stats_start(start=None):
	# Set up for user to enter date
	Start_Date = dt.datetime.strptime(start,"%Y-%m-%d")

	# Query Min, Max, and Avg based on date
	summary_stats = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.round(func.avg(Measurement.tobs))).\
	filter(Measurement.date >= Start_Date).all()
	# Close the Query
	session.close() 
	
	summary = list(np.ravel(summary_stats))

	# Jsonify summary
	return jsonify(summary)

# Same as above with the inclusion of an end date
	# Set up for user to enter dates 
@app.route("/api/v1.0/<start>/<end>")
def stats(start=None, end=None):
	Start_Date=datetime.strptime(start,"%Y-%m-%d")
	end_date=datetime.strptime(end, "%Y-%m-%d")

	# Query Min, Max, and Avg based on dates
	summary_stats = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.round(func.avg(Measurement.tobs))).\
	filter(Measurement.date.between(Start_Date,End_Date)).all()
	# Close the Query
	session.close()    
	
	summary = list(np.ravel(summary_stats))

	# Jsonify summary
	return jsonify(summary)

if __name__ == "__main__":
	app.run()
