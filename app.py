from eth_utils import address
from flask import Flask, render_template, request, redirect, url_for, session
import api

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", user_status=session["loggedin"])


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Logs in user by creating a session
    """
    if session["loggedin"]:
        msg="You are already logged in"
        return render_template('login.html', msg = msg, user_status=session["loggedin"])
    if request.method == "POST" and "address" in request.form and "privat_key" in request.form:
        user_address = request.form["address"]
        user_key = request.form["privat_key"]
        if api.login_user(user_address, user_key):
            session["loggedin"] = True
            session["address"] = user_address
            return redirect(url_for("offers", user_status=session["loggedin"]))
        else:
            msg = "Your address or key was wrong!"
            return render_template('login.html', msg = msg, user_status=session["loggedin"])
    return render_template('login.html',  user_status=session["loggedin"])


@app.route("/logout")
def logout():
    """
    Logs out user and send them to login page 
    """
    session["loggedin"] = False
    msg = "You are now logged out"
    return render_template('login.html', msg = msg, user_status=session["loggedin"])


@app.route("/offers", methods=["GET", "POST"])
def offers():
    """
    Displays offers based on Loggin status 
    """
    if request.method == "POST":
        #redirects users to either buy an offer or change their own based on url
        if "buy/" in request.form["buy_btn"]:
            offer_id = int(request.form["buy_btn"].replace("buy/",""))
            return redirect(url_for("buy", offer_id=offer_id, user_status=session["loggedin"])) 
        elif "change/" in request.form["buy_btn"]:
            offer_id = int(request.form["buy_btn"].replace("change/",""))
            return redirect(url_for("change_offer", offer_id=offer_id, user_status=session["loggedin"]))
    else:
        Offers = api.get_Offers()
        if session["loggedin"]:
            return render_template("offers_loggedin.html", offers=Offers, user_status=session["loggedin"])
        return render_template("offers.html", offers=Offers, user_status=session["loggedin"])


@app.route("/create_offer", methods=["GET", "POST"])
def create_offer():
    """
    Let's users create an offer if they are logged in
    """
    if session["loggedin"]:
        if request.method != "POST":
            user_balance = api.get_Balance_kWh(session["address"])
            return render_template("create_offer.html", user_balance_kWh=user_balance, user_status=session["loggedin"])
        elif request.method == "POST" and "ammount_kWh" in request.form and "price_per_unit" in request.form:
            #gets data from create offer form and sends it to the blockchain
            api.create_Offer(session["address"], request.form["ammount_kWh"], request.form["price_per_unit"])
            user_balance = api.get_Balance_kWh(session["address"])
            msg = "Your offer was successfully created"
            return render_template("create_offer.html", user_balance_kWh=user_balance,
             msg=msg, user_status=session["loggedin"])    
    else:
        msg= "Please login first"
        return  redirect("/login", msg="Please login first", user_status=session["loggedin"])
    

@app.route("/_offer<offer_id>", methods=["GET", "POST"])
def buy(offer_id):
    """
    Let's users buy an offer with the offer id if they are logged in
    """
    if session["loggedin"]:
        if request.method != "POST":
            user_balance_kWh = api.get_Balance_kWh(session["address"])
            user_balance_eth = api.get_Balance_eth(session["address"])
            offer = api.get_Offer(offer_id)
            return render_template("buy.html", msg_kWh=user_balance_kWh,
             msg_eth=user_balance_eth, offers=offer,  user_status=session["loggedin"])
        else:
            api.buy_Offer(session["address"],offer_id)
            msg="Thank you for your purchase"
            return redirect(url_for(".account", msg=msg,  user_status=session["loggedin"]))
    else:
        msg= "Please login first"
        return redirect("/login", msg=msg, user_status=session["loggedin"])


@app.route("/change_offer<offer_id>", methods=["GET", "POST"])
def change_offer(offer_id):
    """
    Let's users change an offer with the offer id if they are logged in
    """
    if session["loggedin"]:
        if request.method != "POST":
            user_balance_kWh = api.get_Balance_kWh(session["address"])
            offer = api.get_Offer(offer_id)
            return render_template("change_offer.html", user_balance_kWh=user_balance_kWh,
             offers=offer,  user_status=session["loggedin"])
        else:
            offer = api.get_Offer(offer_id)
            unit_price = request.form["price_per_unit"]
            if "price_per_unit" in request.form:
                api.change_Offer_price(offerID=offer_id,user_address=session["address"], price_unit=unit_price)
            msg = f"The unit price was changed to {unit_price}"
            return redirect(url_for(".account", msg=msg,  user_status=session["loggedin"]))
    else:
        msg= "Please login first"
        return redirect("/login", msg=msg,  user_status=session["loggedin"])


@app.route("/account")
def account():
    """
    Display account data if user is signed in 
    """
    if session["loggedin"]:
        try:
            msg = request.args["msg"]
        except:
            msg=""
        user_balance_kWh = api.get_Balance_kWh(session["address"])
        user_balance_eth = api.get_Balance_eth(session["address"])
        Offers = api.get_user_Offers(session["address"])
        return render_template("account.html", msg_kWh=user_balance_kWh,
             msg_eth=user_balance_eth, msg=msg,
             offers=Offers, user_status=session["loggedin"])  
    else:
        msg="Please log in first"
        return  redirect("/login", msg=msg, user_status=session["loggedin"])


if __name__ == "__main__":
    app.secret_key = '09121998'
    app.run(debug=True)