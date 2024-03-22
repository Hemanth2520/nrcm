from flask import *
import pymysql
app=Flask(__name__) 

# CONNECTING DATABASE
mydb=pymysql.connect(host="localhost",user="root",password="",database="nrcm")
cursor = mydb.cursor()
if mydb:
    print("connected")
else:
    print("not connected")
@app.route("/",methods=["GET","POST"]) # for routing to the homepage of our website
def login():
    if request.method=="POST":
        roll=request.form["user"]
        cursor.execute("SELECT * FROM users where roll_number='%s'",(roll))
        data=cursor.fetchone()
        print(data)
    return render_template("index.html")

@app.route("/dashboard")
def dash():
    return render_template("dashboard.html")



if __name__ =="__main__":
    app.run(debug=True)