from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from database import UserDatabase

app = Flask(__name__)
app.secret_key = "bdf7177bde6923b8e44bcd97b60f48cf48f3f7f36ecb7ce52563bbc99b80658d" # Change this
userdb = UserDatabase()


@app.route("/")
def loginPage():
    return render_template("login.html")

@app.route("/login",methods=["POST"])
def login():

    # Get the post data (hopefully its a form or the users gonnna have a bad day)
    data = dict(request.form)
    success, token = userdb.login(data["username"], data["password"])

    # Set the token in the cookies and take our user to the index
    if success:
        response = make_response(redirect("home"))
        age =  60* 60 * 24 * 7 # 1 week 
        response.set_cookie("__token", token, age, httponly=True)
        return response
    
    # Flash an error
    else:
        flash("ERROR: Incorrect username or password, please try again :)", "error") # Show error message
        return redirect(url_for("/")) # Redirect back to index (login page)
    
@app.route("/home")
def homePage():
    print("USER TRYING TO ACCESS HOMEPAGE")
    token = str(request.cookies.get("__token", ""))
    # if the token is valid go to the homepage else return us back to the login page
    if userdb.isValidToken(token=token):
        return render_template("homepage.html")
    else:
        flash("Access token is not valid, please try logging in again   ", "ERROR")
        return redirect(url_for("loginPage"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    