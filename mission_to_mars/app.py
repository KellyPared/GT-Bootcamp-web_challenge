from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import re


app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_dictionary"
mongo = PyMongo(app,uri = "mongodb://localhost:27017/mars_dictionary")



@app.route("/")
def index():
    # find one document from our mongo db and return it.
    mars_dictionary_db = mongo.db.mars_dictionary_db.find_one()
    # pass mars to render_template
    return render_template("index.html", mars_dictionary_db=mars_dictionary_db)

# set our path to /scrape
@app.route("/scrape")
def scrape():
    # create a mars database
    mars_dictionary_db = mongo.db.mars_dictionary_db
    # call the scrape function in our scrape_phone file. This will scrape and save to mongo.
    mars_data = scrape_mars.scrape()
    # update our listings with the data that is being scraped.
    mars_dictionary_db.replace_one({}, mars_data, upsert=True)
    # return a message to our page so we know it was successful.
    return redirect("/",code=302)


if __name__ == "__main__":
    #host='0.0.0.0', port=8070,
    app.run(debug=True)
