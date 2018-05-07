from flask import Flask, jsonify

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)





# 1. import Flask and jsonify
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func



#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///../hawaii.sqlite', )

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Create our session (link) from Python to the DB
session = Session(engine)
# Print all of the classes mapped to the Base
Base.classes.keys()
# Save reference to the table

Measurement_Station_Join = Base.classes.measurement_station_join


#################################################
# Flask Setup
#################################################
app = Flask(__name__)




# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to my 'Home' page!  \n 1. /about \n 2. /api/v1.0/precipitation \n  3. /api/v1.0/stations  \n 4.  /api/v1.0/tobs  5./api/v1.0/<start>   6. /api/v1.0/delta"



# 4. Define what to do when a user hits the /about route
@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"



#/api/v1.0/precipitation route 
@app.route("/api/v1.0/precipitation")
#Query for the dates and temperature observations from the last year.
##Convert the query results to a Dictionary using date as the key and prcp as the value.
###Return the json representation of your dictionary.

def precipitation():
    #query dates and temp for the last year
    results= session.query(Measurement_Station_Join.date,Measurement_Station_Join.prcp).\
        filter(Measurement_Station_Join.date <="2017/5/8").\
        filter(Measurement_Station_Join.date >="2016/5/8").all()

    # Convert list of tuples into normal list
    all_data = list(np.ravel(results))

    return jsonify(all_data)

#/api/v1.0/stations
''' get all data for stations and return in api '''
@app.route("/api/v1.0/stations")

def stations():
    #query list of all stations
    results= session.query(Measurement_Station_Join.station,Measurement_Station_Join.name).\
                          group_by(Measurement_Station_Join.station).all()
    
    all_data=list(np.ravel(results))

    return jsonify(all_data)

#'''/api/v1.0/tobs''''
#query all of tobs data for the past year
@app.route("/api/v1.0/tobs")
def tobs():
    results= session.query(Measurement_Station_Join.date,Measurement_Station_Join.tobs).\
        filter(Measurement_Station_Join.date <="2017/5/8").\
        filter(Measurement_Station_Join.date >="2016/5/8").all()
    all_data=list(np.ravel(results))

    return jsonify(all_data)


#/api/v1.0/<start> 
@app.route("/api/v1.0/<start>")

def calc_temps(start):   
    results=session.query(Measurement_Station_Join.date,Measurement_Station_Join.tobs).\
               filter(Measurement_Station_Join.date== "2016/5/6").\
               order_by(Measurement_Station_Join.date).all()

    #all_data=list(np.ravel(results))

    #return jsonify(all_data)



#get averages for all the data
    dates=[]
    temp=[]
    max_temp=0
    min_temp=0
    average_temp=0

    for i in results:
        a,b=i
        dates.append(a)
        temp.append(b)

    max_temp=max(temp)
    min_temp=min(temp)
    average_temp=(sum(temp)/len(temp))
    
    return (f'|||| Max temp:{max_temp}F  ||||   Min temp:{min_temp}F   |||| Average temp:{average_temp}F ||||')
    

#/api/v1.0/<start>/<end> 
@app.route("/api/v1.0/delta")

def calc_temps_diff():   
    results=session.query(Measurement_Station_Join.date,Measurement_Station_Join.tobs).\
       filter(Measurement_Station_Join.date >= "2016/5/6").\
       filter(Measurement_Station_Join.date <= "2017/5/6").all()

#get averages for all the data
    dates_b=[]
    temp_b=[]
    max_temp_b=0
    min_temp_b=0
    average_temp_b=0

    for i in results:
        a,b=i
        dates_b.append(a)
        temp_b.append(b)

    max_temp_b=max(temp)
    min_temp_b=min(temp)
    average_temp_b=(sum(temp)/len(temp))
    
    return (f'|||| Max temp:{max_temp_b}F  ||||   Min temp:{min_temp_b}F   |||| Average temp:{average_temp_b}F ||||')
    

#thats it




if __name__ == "__main__":
    app.run(debug=True)
