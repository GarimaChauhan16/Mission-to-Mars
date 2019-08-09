from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/Mars_App")


# Route to render index.html template using data from Mongo
@app.route("/")
def index():
     # Find one record of data from the mongo database
    mars = mongo.db.mars.find_one()
    print(mars)

    # Return template and data
    return render_template("index.html", mars_data=mars)

# Route that will trigger the scrape function


@app.route("/scrape")
def scraper():
    # Run the scrape function and save the results to a variable
    results = scrape_mars.mars_scrape()


    # Update the Mongo database using update and upsert=True
    mongo.db.mars.update({}, results, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)