from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
scraped_date = scrape_mars.today()

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    print("Launch in 3..2..1...!!")
    return render_template("index.html", mars=mars, scraped_date=scraped_date)

# Scrape for News
@app.route("/scrape")
def scraper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/landed", code=302)

# Final result
@app.route("/landed")
def result():
    mars = mongo.db.mars.find_one()
    return render_template("result.html", mars=mars, scraped_date=scraped_date)

if __name__ == "__main__":
    app.run(debug=True)