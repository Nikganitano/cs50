import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Retrieve form data
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")
        
        # Insert the new row into the birthdays table
        db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", name, month, day)
        
        # Redirect the user back to the home page
        return redirect("/")
    else:
        # Query the database for all birthdays
        birthdays = db.execute("SELECT name, month, day FROM birthdays")
        
        # Pass the data to the index.html template
        return render_template("index.html", birthdays=birthdays)
    
@app.route('/clear', methods=['POST'])
def clear_birthdays():
    # Clear the birthdays table
    db.execute("DELETE FROM birthdays")
    
    # Redirect the user back to the home page
    return redirect("/") 

if __name__ == "__main__":
    app.run(debug=True)
