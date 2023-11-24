# Date: 11/16/2023
# Adapted from
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os
from flask import flash

app = Flask(__name__)

# Database connection information

# Uncomment below for DK 
# app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
# app.config["MYSQL_USER"] = "cs340_kimda6"
# app.config["MYSQL_PASSWORD"] = "2371"
# app.config["MYSQL_DB"] = "cs340_kimda6"
# app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# Uncomment below for Brian 
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_kimda6"
app.config["MYSQL_PASSWORD"] = "2371"
app.config["MYSQL_DB"] = "cs340_kimda6"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Routes
# Homepage route to /gyms by default
@app.route("/")
def home():
    return redirect("/gyms")

# Route for Gyms page
@app.route("/gyms", methods = ["POST", "GET"])
def gyms():

    # Retrieve and display the data
    if request.method == "GET":
        # Query to get all information in Gyms entity (gym_ID, location, email, opening/closing time)
        query = "select * from Gyms"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("gyms.j2", data = data)

    # Add a new gym
    if request.method == "POST":
        # Add gym button is selected, get user input
        if request.form.get("Add_Gym"):
            location = request.form["location"]
            email = request.form["email"]
            opening_time = request.form["opening_time"]
            closing_time = request.form["closing_time"]

            query = "insert into Gyms(location, email, opening_time, closing_time) values (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (location, email, opening_time, closing_time))
            mysql.connection.commit()

            # Redirect back to Gyms page
            return redirect("/gyms")

@app.route("/delete_gym/<int:id>")
def delete_gym(id):
    #mySQL query to delete the gym with our passed id
    query = "DELETE FROM Gyms where gym_ID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,)) 
    mysql.connection.commit() 

    #redirect back to gyms page 
    return redirect("/gyms") 

@app.route("/edit_gym/<int:id>", methods=["POST", "GET"])
def edit_gym(id):
    if request.method == 'GET':
        #mySQL query to grab the info of the person w/our passed id 
        query = "SELECT * from Gyms where gym_ID = %s" % (id) 
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall() 
    
    # dropdown code here 

        return render_template("edit_gyms.j2", data=data)
    
    #the 'meat and potatoes' of our update functionality
    if request.method == 'POST': 
        #fire off if user clicks the Edit Person button
        if request.form.get("edit_gym"): 
            #grab user form inputs 
            id = request.form["gym_ID"]
            location = request.form["location"]
            email = request.form["email"]
            opening_time = request.form["opening_time"]
            closing_time = request.form["closing_time"] 

            #for testing purposes, do not put NULL for any of the input.
            query = "UPDATE Gyms SET Gyms.location = %s, Gyms.email = %s, Gyms.opening_time = %s, Gyms.closing_time = %s where gym_ID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (location, email, opening_time, closing_time, id))
            mysql.connection.commit() 
            
        return redirect("/gyms")


# Route for Members page
@app.route("/members", methods = ["POST", "GET"])
def members():
    if request.method == "GET":
        query = "select * from Members"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("members.j2", data=data)


    if request.method == 'POST': 
        if request.form.get("Add_Member"): 
            first_name =request.form["first_name"]
            last_name = request.form["last_name"]
            age = request.form["age"]
            email = request.form["email"]
            gender = request.form["gender"]

            query = "insert into Members (first_name, last_name, age, email, gender) values (%s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (first_name, last_name, age, email, gender))
            mysql.connection.commit()

            return redirect("/members")
        
@app.route("/delete_member/<int:id>")
def delete_member(id):
    query = "DELETE from Members where member_ID = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/members")
        
@app.route("/edit_member/<int:id>", methods=["POST", "GET"])
def edit_member(id):
    if request.method == 'GET':
        query = "SELECT * from Members where member_ID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall() 

        return render_template("edit_members.j2", data=data)


    if request.method == 'POST':
        if request.form.get("edit_member"):
            id = request.form["member_ID"]
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            age = request.form['age']
            email = request.form['email']
            gender = request.form['gender']

            query = "update Members SET Members.first_name = %s, Members.last_name = %s, Members.age = %s, Members.email = %s, Members.gender = %s where member_ID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (first_name, last_name, age, email, gender, id))
            mysql.connection.commit() 

        return redirect("/members")


# Route for Courts page
@app.route("/courts", methods = ["POST", "GET"])
def courts():
    if request.method == "GET":
        query = "select * from Courts order by gym_ID asc"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Query to get a dropdown list of gym locations
        query2 = "select gym_ID, location from Gyms"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        gym_location_data = cur.fetchall()

        return render_template("courts.j2", data=data, locations=gym_location_data)

    if request.method == 'POST': 
        if request.form.get("Add_Court"): 
            gym_ID =request.form["gym_ID"]
            court_name = request.form["court_name"]

            query = "insert into Courts (gym_ID, court_name) values (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (gym_ID, court_name))
            mysql.connection.commit()

            return redirect("/courts")

@app.route("/edit_court/<int:id>", methods=["POST", "GET"])
def edit_court(id):
    if request.method == 'GET':
        # SQL query to get info of Courts from court ID
        query = "SELECT * from Courts where court_ID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall() 

        # SQL query to get dropdown of gym locations
        query2 = "SELECT gym_ID, location from Gyms"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        gym_location_data = cur.fetchall()

        # Return edit_courts page passing query data and gym location data to the edit_courts page
        return render_template("edit_courts.j2", data=data, locations=gym_location_data)

    if request.method == "POST":
        if request.form.get("edit_court"):
            id = request.form["court_ID"]
            location = request.form["gym_location"]
            court_name = request.form["court_name"]

            # query = "update Courts set Courts.gym_ID = (SELECT gym_ID FROM Gyms where Gyms.location = %s), Courts.court_name = %s where court_ID = %s"
            query = "update Courts set Courts.gym_ID = Courts.gym_ID = %s, Courts.court_name = %s where court_ID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (location, court_name, id))
            mysql.connection.commit()

        return redirect("/courts")

# @app.route("/delete_court/<int:id>")
# def delete_court(id):
#     query = "DELETE from Courts where court_ID = %s;"
#     cur = mysql.connection.cursor()
#     cur.execute(query, (id,))
#     mysql.connection.commit()

#     return redirect("/courts")

@app.route("/gymmemberships", methods = ["POST", "GET"])
#GymMemberships table will allow us to add a row into GymMemberships using 2 dropdowns:
# 1 for each FK. A dropdown for gym_ID, and a dropdown for member_ID
# Then it will execute sql query:
# "insert into GymMemberships (gym_ID, member_ID)
# values (
# (select gym_ID from Gyms where loaction="(FIRST_DROPDOWN)"), 
# select member_ID from Members where first_name="(SECOND_DROPDOWN)")
# ); 
def gymmemberships(): 
    if request.method == "GET":
        query = "select * from GymMemberships" 
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        
        # query2 = "Select gym_ID, gym_memberships_ID FROM GymMemberships "
        query2 = "Select location FROM Gyms"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        gym_location_data = cur.fetchall()

        
        return render_template("gymmemberships.j2", data=data, locations=gym_location_data)
    
    if request.method == "POST":
        selected_gym_id = request.form.get('choice_gyms')
        query3 = "SELECT member_ID from GymMemberships where gym_ID = %s"
        cur = mysql.conneciton.cursor()
        cur.execute(query3, (selected_gym_id,))
        gyms_members_data = cur.fetchall()

        return render_template("gymmemberships.j2", data=gym_members_data, locations=gym_location_data)




if __name__ == "__main__":
    app.run(port = 5281, debug = True) 
    # Use local (specify port above^) or use 5282 for development / 5280 is for submission 
    # port 5280 was for the Proj step 4 submission. Make sure to start the app there when done.
    # you can also run app.py (change the port# i,e. to 5281) to have it run on local machine so that you don't have to kill gunicorn 
    # and re-run each time to show changes 
