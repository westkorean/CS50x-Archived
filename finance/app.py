import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    stocks = db.execute("SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)

    portfolio = []
    total_value = 0

    for stock in stocks:
        stock_info = lookup(stock["symbol"])
        stock_value = stock["total_shares"] * stock_info["price"]
        total_value += stock_value
        portfolio.append({
            "symbol": stock["symbol"],
            "shares": stock["total_shares"],
            "price": stock_info["price"],
            "total": stock_value
        })

    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
    total_value += user_cash

    return render_template("index.html", stocks=portfolio, cash=user_cash, total=total_value)




@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # Get symbol and shares from form
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Validate inputs
        if not symbol:
            return apology("must provide symbol", 400)

        try:
            shares = int(shares)
            if shares <= 0:
                return apology("invalid number of shares", 400)
        except ValueError:
            return apology("invalid number of shares", 400)

        # Lookup stock price
        stock = lookup(symbol.upper())
        if stock is None:
            return apology("invalid stock symbol", 400)

        # Calculate total price
        total_price = stock["price"] * shares

        # Get user's current cash balance
        user_id = session["user_id"]
        user = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = user[0]["cash"]

        # Check if user has enough money
        if cash < total_price:
            return apology("not enough cash", 400)

        # Update user's cash balance
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_price, user_id)

        # Insert transaction into database
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, transaction_type, timestamp) VALUES (?, ?, ?, ?, ?, datetime('now'))",
           user_id, stock["symbol"], shares, stock["price"], "BUY")

        # Flash success message and redirect to home page
        flash(f"Bought {shares} shares of {stock['symbol']} for {usd(total_price)}", "success")
        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")

        stock = lookup(symbol)
        if not stock:
            return apology("Invalid stock symbol", 400)

        return render_template("quoted.html", stock=stock, price=usd(stock["price"]))

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return apology("Missing username or password", 400)

        if password != confirmation:
            return apology("Passwords do not match", 400)

        # Hash password
        hash = generate_password_hash(password)

        # Insert new user into database
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except:
            return apology("Username already exists", 400)

        return redirect("/login")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]
    stocks = db.execute("SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        user_shares = next((stock["total_shares"] for stock in stocks if stock["symbol"] == symbol), 0)

        if shares > user_shares:
            return apology("Not enough shares", 400)

        stock = lookup(symbol)
        total_sale = stock["price"] * shares

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)", user_id, symbol, -shares, stock["price"])
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_sale, user_id)

        return redirect("/")

    return render_template("sell.html", stocks=stocks)

