import os

import pandas as pd
import numpy as np
import pymongo

from flask import Flask, jsonify, render_template,Response, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from bson.son import SON


app = Flask(__name__)


#################################################
# Database Setup
#################################################

#Making Mongo DB connections
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

#Creating DB
db = client.rent_DB

#Creating collections for the DB
craigslist_collection = db.craigs.find()


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")




@app.route('/rent_by_city')
def city():
    return render_template("rent_by_city.html")

@app.route('/rent_by_region')
def region():
    return render_template("rent_by_region.html")


#=========================
@app.route("/map")
def map():
    """Return the homepage."""
    return render_template("rental_maps.html")

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route("/alldata")
def maps():
    print("Print")
    lista = []
    rent_list = db.craigslist_collection.find()
    for i in list(rent_list):
        dic = {}
        for j,k in i.items():
            if not j == "_id":
                dic[j] = k
        lista.append(dic)
    
    return jsonify(lista[1:10])    	
	
#======================	






@app.route("/names")
def names():
    """Return a list of sample names."""


    return jsonify(db.craigslist_collection.distinct('City'))


@app.route("/region")
def regions():
    """Return a list of sample names."""


    return jsonify(db.craigslist_collection.distinct('Region'))



@app.route("/regioncount")
def samples():
    
    """Return `otu_ids`, `otu_labels`,and `sample_values`."""
    query = [{"$unwind": "$City"},
                {"$group": {"_id": "$City", "count": {"$sum": 1}}}, 
                {"$sort": SON([("count", -1), ("_id", -1)])}]
    labels = []
    values = []
    for data in list(db.craigslist_collection.aggregate(query))[:10]:
        
        labels.append(data["_id"])
        values.append(data["count"])
    trace = {"labels": labels, "values": values}
    return jsonify(trace)


@app.route("/cityavgprice")
def sample():
    
    """Return `otu_ids`, `otu_labels`,and `sample_values`."""
    query = [{"$group": {"_id":"$City","avg_price": {"$avg": "$price"}}},
         {"$sort": SON([("count", -1), ("avg_price", -1)])}]
    
    labels = []
    values = []
    
    for data in list(db.craigslist_collection.aggregate(query))[1:11]:
        
        labels.append(data["_id"])
        values.append(int(data["avg_price"]))
    trace = {"labels": labels, "values": values}
    
    return jsonify(trace)

   
@app.route("/metadata/<sample>")
def sample_metadata(sample):
    dic = {}
    #Get Maximum price for the city
    max_p = [{"$match" : {"City":sample}},
             {"$group" : {"_id": "$City","max_rent" : {"$max" : "$price"}}}]

    max_price = list(db.craigslist_collection.aggregate(max_p))

    #Get Minimum price for the city
    min_p = [{"$match" : {"City":sample}},
             {"$group" : {"_id": "$City","min_rent" : {"$min" : "$price"}}}]

    min_price = list(db.craigslist_collection.aggregate(min_p))

    #Get Average Price for the city
    avg_price = [{"$match" : {"City":sample}},
                 {"$group" : {"_id": "$City","avg_rent" : {"$avg" : "$price"}}}]
    avg_price = list(db.craigslist_collection.aggregate(avg_price))

    #Get Bedroom Details

    bed = {}
    for xbeds in [0,1,2,3]:
        beds = [{"$match" : {"City":sample}},{"$match" : {"bedrooms":xbeds}},
            {"$group": {"_id":"$City","Total_bedroom": {"$sum": 1}}}]

        tot_bedroom_by_city = db.craigslist_collection.aggregate(beds)
    
        output = list(tot_bedroom_by_city)
        if output:
           
            bed[xbeds] = output[0]["Total_bedroom"]



    #Save All data to dictionary
    if 0 in bed:
        dic["Studio"] = bed[0]
    if 1 in bed:
        dic["One bed"] = bed[1]
    if 2 in bed:
        dic["Two beds"] = bed[2]
    if 3 in bed:
        dic["Three beds"] = bed[3]

    

    dic["Highest Price"] = max_price[0]["max_rent"]
    dic["Lowest Price"] = min_price[0]["min_rent"]
    dic["Average Price"] = round(avg_price[0]["avg_rent"],2)
    return jsonify(dic)

@app.route("/regiondata/<sample>")
def sample_regiondata(sample):
    dic = {}
    #Get Maximum price for the city
    max_p = [{"$match" : {"Region":sample}},
             {"$group" : {"_id": "$Region","max_rent" : {"$max" : "$price"}}}]

    max_price = list(db.craigslist_collection.aggregate(max_p))

    #Get Minimum price for the city
    min_p = [{"$match" : {"Region":sample}},
             {"$group" : {"_id": "$Region","min_rent" : {"$min" : "$price"}}}]

    min_price = list(db.craigslist_collection.aggregate(min_p))

    avg_price = [{"$match" : {"Region":sample}},
                 {"$group" : {"_id": "$Region","avg_rent" : {"$avg" : "$price"}}}]
    avg_price = list(db.craigslist_collection.aggregate(avg_price))

    #Get Bedroom Details

    bed = {}
    for xbeds in [0,1,2,3]:
        beds = [{"$match" : {"Region":sample}},{"$match" : {"bedrooms":xbeds}},
            {"$group": {"_id":"$Region","Total_bedroom": {"$sum": 1}}}]

        tot_bedroom_by_city = db.craigslist_collection.aggregate(beds)
    
        output = list(tot_bedroom_by_city)
        if output:
            
            bed[xbeds] = output[0]["Total_bedroom"]



    #Save All data to dictionary
    if 0 in bed:
        dic["Studio"] = bed[0]
    if 1 in bed:
        dic["One bed"] = bed[1]
    if 2 in bed:
        dic["Two beds"] = bed[2]
    if 3 in bed:
        dic["Three beds"] = bed[3]


    dic["Highest Price"] = max_price[0]["max_rent"]
    dic["Lowest Price"] = min_price[0]["min_rent"]
    dic["Average Price"] = round(avg_price[0]["avg_rent"],2)
    return jsonify(dic)





if __name__ == "__main__":
    app.run()
