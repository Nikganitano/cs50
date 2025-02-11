import os
import logging

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///budget.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show budget overview"""
    user_id = session["user_id"]
    
    # Fetch the user's cash and budget
    user = db.execute("SELECT cash, budget FROM users WHERE id = ?", user_id)
    
    # Check if the user exists
    if not user:
        flash("User not found", "error")
        return redirect("/logout")  # Redirect to logout or another appropriate page
    
    cash = float(user[0]["cash"])
    budget = float(user[0]["budget"])
    
    # Fetch the user's budget movements
    movements = db.execute("SELECT category, amount, description, date FROM budget_movements WHERE user_id = ?", user_id)
    
    # Calculate the total amount of all movements
    total_amount = sum(movement["amount"] for movement in movements)
    
    # Update the remaining cash based on the movements
    remaining_cash = budget - total_amount
    
    # Update the user's cash in the database
    db.execute("UPDATE users SET cash = ? WHERE id = ?", remaining_cash, user_id)
    
    return render_template("index.html", movements=movements, cash=remaining_cash, total_amount=total_amount, budget=budget)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_movement():
    if request.method == 'POST':
        # Handle the form submission to add a movement
        category = request.form['category']
        amount = float(request.form['amount'])  # Convert amount to float
        description = request.form['description']
        user_id = session["user_id"]

        # Add the movement to the database
        db.execute("INSERT INTO budget_movements (user_id, category, amount, description) VALUES (?, ?, ?, ?)",
                   user_id, category, amount, description)

        # Update the remaining cash in the users table
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", amount, user_id)

        flash('Movement added successfully', 'success')
        return redirect('/')

    # Check if a budget is set
    user_id = session["user_id"]
    budget = db.execute("SELECT budget FROM users WHERE id = ?", user_id)
    budget_set = budget and budget[0]['budget'] is not None

    return render_template('add.html', budget_set=budget_set)


@app.route("/balance")
@login_required
def balance():
    """Show balance overview"""
    user_id = session["user_id"]
    
    # Fetch the user's cash
    user = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    
    # Check if the user exists
    if not user:
        flash("User not found", "error")
        return redirect("/logout")  # Redirect to logout or another appropriate page
    
    cash = user[0]["cash"]
    
    # Fetch the user's budget movements
    movements = db.execute("SELECT category, amount, description, date FROM budget_movements WHERE user_id = ?", user_id)
    
    # Group movements by category and calculate totals
    movements_by_category = {}
    totals_by_category = {}
    for movement in movements:
        category = movement["category"]
        if category not in movements_by_category:
            movements_by_category[category] = []
            totals_by_category[category] = 0
        movements_by_category[category].append(movement)
        totals_by_category[category] += movement["amount"]
    
    return render_template("balance.html", movements_by_category=movements_by_category, totals_by_category=totals_by_category, cash=cash)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/set-budget", methods=["GET", "POST"])
@login_required
def set_budget():
    user_id = session["user_id"]

    if request.method == "POST":
        # Get the new budget amount from the form
        amount = float(request.form["amount"])

        # Update the user's budget and cash
        db.execute("UPDATE users SET budget = ?, cash = ? WHERE id = ?", amount, amount, user_id)

        flash("Budget set successfully", "success")
        return redirect("/")

    # Fetch the user's current budget and cash
    user = db.execute("SELECT budget, cash FROM users WHERE id = ?", user_id)
    if not user:
        flash("User not found", "error")
        return redirect("/logout")  # Redirect to logout or another appropriate page

    budget = float(user[0]["budget"])
    cash = float(user[0]["cash"])

    # Calculate remaining cash
    remaining_cash = cash

    return render_template("set-budget.html", budget=budget, remaining_cash=remaining_cash)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Must Give Username")

        if not password:
            return apology("Must Give Password")

        if not confirmation:
            return apology("Must Give Confirmation")

        if password != confirmation:
            return apology("Password Do Not Match")

        hash = generate_password_hash(password)

        try:
            new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except:
            return apology("Username already exists")
        session["user_id"] = new_user

        return redirect("/")


@app.route("/remove", methods=["GET", "POST"])
@login_required
def remove():
    """Remove a budget movement"""
    user_id = session["user_id"]
    
    if request.method == "POST":
        movement_id = request.form.get("movement_id")

        # Validate form input
        if not movement_id:
            flash("Movement ID is required", "error")
            return redirect("/remove")

        # Remove the movement from the database
        db.execute("DELETE FROM budget_movements WHERE id = ? AND user_id = ?", movement_id, user_id)

        flash("Movement removed successfully", "success")
        return redirect("/balance")

    # Fetch the user's movements to display in the dropdown
    movements = db.execute("SELECT id, category, amount, date FROM budget_movements WHERE user_id = ?", user_id)
    return render_template("remove.html", movements=movements)


@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    logging.debug("change-password function called")
    
    if request.method == 'POST':
        logging.debug("POST request received")
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_new_password = request.form['confirm_password']

        try:
            # Query database for user
            user_id = session["user_id"]
            user = db.execute("SELECT * FROM users WHERE id = ?", user_id)

            # Check if the current password is correct
            if not user or not check_password_hash(user[0]['hash'], current_password):
                flash('Current password is incorrect', 'error')
                logging.warning("Current password is incorrect for user_id: %s", user_id)
                return redirect('/change-password')

            # Check if the new passwords match
            if new_password != confirm_new_password:
                flash('New passwords do not match', 'error')
                logging.warning("New passwords do not match for user_id: %s", user_id)
                return redirect('/change-password')

            # Update the password
            new_password_hash = generate_password_hash(new_password)
            db.execute("UPDATE users SET hash = ? WHERE id = ?", new_password_hash, user_id)

            flash('Your password has been updated', 'success')
            logging.info("Password updated successfully for user_id: %s", user_id)
            return redirect('/')

        except Exception as e:
            logging.error("Error updating password for user_id: %s, error: %s", user_id, str(e))
            flash('An error occurred while updating your password. Please try again.', 'error')
            return redirect('/change-password')

    logging.debug("Rendering change-password.html template")
    return render_template('change-password.html')

# Assuming db and other necessary configurations are set up here

if __name__ == '__main__':
    app.run(debug=True)