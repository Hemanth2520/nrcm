from flask import *
import pymysql
app=Flask(__name__) 

# CONNECTING DATABASE
mydb=pymysql.connect(host="localhost",user="root",password="",database="hemanth")
cursor = mydb.cursor()
is_login=False
userid=""
rollnumber=""
userroll=""

if mydb:
    print("connected")
else:
    print("not connected")

@app.route("/",methods=["GET","POST"]) # for routing to the homepage of our website
def login():
    error=""
    if request.method=="POST":
        roll=request.form["user"]
        cursor.execute("SELECT * FROM users where roll_number=%s",(roll))
        data=cursor.fetchone()
        print(data)
        if data==None:
            error="Invalid user"
        else:
            global is_login
            global userid
            global userroll
            global rollnumber

            is_login=True
            userid=data[0]
            rollnumber=data[2]
            userroll=data[6]

            return redirect("dashboard")
    return render_template("index.html",data=error)

@app.route("/dashboard")
def dashboardpage():
    if is_login:
        cursor.execute("SELECT * FROM users where roll_number=%s",(rollnumber,))
        userData=cursor.fetchone()
        return render_template("dashboard.html",userdata=userData)
    else:
        return redirect("/")
    




@app.route('/register', methods=['GET', 'POST'])
def reg():
    msg=""
    if request.method=="POST":
        username=request.form['username']
        roll=request.form['roll_number']
        email=request.form['email']
        password=request.form['password']
        try:
            cursor.execute("INSERT INTO users (username, roll_number, email, password) VALUES (%s, %s, %s, %s)", (username, roll, email, password))
            msg=1
            mydb.commit()
        except:
            msg=0
    return render_template('form.html',msg=msg)

@app.route("/retrive",methods=["GET","POST"]) # for routing to the homepage of our website
def getdeatails():
    retrive_data=""
    if request.method=="POST":
        roll=request.form["roll_number"]
        cursor.execute("SELECT * FROM users where roll_number=%s",(roll))
        retrieve=cursor.fetchone()
        # print(retrieve)
        if retrieve==None:
           retrive_data="Invalid roll"
        else:
            # global is_getdetails
            # is_getdetails=True
            retrive_data=retrieve
    return render_template("formget.html",retrieve=retrive_data)


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method=="POST":
        username=request.form['username']
        roll=request.form['roll_number']
        email=request.form['email']
        password=request.form['password']
        cursor.execute("UPDATE users set username=%s,password=%s,email=%s where roll_number= %s ",(username,password,email,roll))
        mydb.commit()
        
    return render_template('form.html')

@app.route("/users") # for routing to the homepage of our website
def userlist():
    cursor.execute("SELECT * FROM users" )
    data=cursor.fetchall()
    return render_template("formsretrival.html",users=data)


@app.route("/myinfo")
def details():
    if is_login:
        cursor.execute("SELECT * FROM users where roll_number=%s",(rollnumber,))
        userData=cursor.fetchone()
        return render_template("information.html",user=userData)
    else:
        return redirect("/")
    

@app.route("/editinfo",methods=["GET","POST"])
def edit():
    uid=request.args.get('id')
    if request.method=="POST":
        username=request.form['username']
        email=request.form['email']
        try:
            cursor.execute("UPDATE  users SET username=%s,email=%s where id=%s",(username,email,uid))
            mydb.commit()
            return redirect("/users")
        except:
            return redirect("/users")
    userData=cursor.fetchone()
    return render_template("edit.html",user=userData)

@app.route("/deluser",methods=["GET","POST"])
def  deleteUser():
    userid=request.args.get('id')
    try:
        cursor.execute("DELETE FROM users WHERE id= %s ", (userid,))
        mydb.commit()
        return redirect("/users")
    except Exception as e:
        print(str(e))
        return redirect("/users")

if __name__ =="__main__":
    app.run(debug=True)