# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 11:34:42 2023

@author: sdvpr
"""

from flask import Flask, request, render_template,request,session
import ibm_db

app = Flask(__name__)
app.secret_key = "_ab+d=5"
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;UID=yfj04792;PWD=b5pYMzx1ZBhjWCGt;SECURITY=SSL;SSLCERTIFICATE=DigiCertGlobalRootCA.crt",'','')
print(conn)
print(ibm_db.active(conn))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        global uname
        uname = request.form['username']
        pword = request.form['password']
        print(uname, pword)
        sql = "SELECT * FROM REG WHERE USERNAME = ? AND PASSWORD = ?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1, uname)
        ibm_db.bind_param(stmt,2,pword)
        ibm_db.execute(stmt)
        out = ibm_db.fetch_assoc(stmt)
        print(out)
        if out != False:
            session['username'] = uname
            session['emailid'] = out['EMAIL']
            
            if out['ROLE'] == "admin":
                return render_template("adminprofile.html",adname = out['NAME'], ademail = out['EMAIL'] )
            elif out['ROLE'] == "student":
                return render_template("studentprofile.html",sname = out['NAME'], semail = out['EMAIL'])
            else: 
                return render_template("facultyprofile.html",fname = out['NAME'], femail = out['EMAIL'])
        else: 
            msg = "Invalid Credentials"
            return render_template("login.html",message1= msg)
    return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def regsiter():
    if request.method == "POST":
        name = request.form['NAME']
        email = request.form['EMAIL']
        uname = request.form['USERNAME']
        pword = request.form['PASSWORD']
        role = request.form['ROLE']
        print(uname,email,pword,role,name)
        sql = "SELECT * FROM REG WHERE USERNAME=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1, uname)
        ibm_db.execute(stmt)
        out = ibm_db.fetch_assoc(stmt)
        print(out)
        if out != False:
            msg = "Already Registered"
            return render_template("register.html", message2 = msg)
        else: 
            print("hi")
            sql = "INSERT INTO REG VALUES(?,?,?,?,?)"
            print("hello")
            stmt = ibm_db.prepare(conn, sql)
            print("ggggg")
            ibm_db.bind_param(stmt, 1, name)
            ibm_db.bind_param(stmt, 2, email)
            ibm_db.bind_param(stmt, 3, uname)
            
            print("scxzc")
            ibm_db.bind_param(stmt, 4, pword)
            ibm_db.bind_param(stmt, 5, role)
            
            ibm_db.execute(stmt)
            print("done")
            msg = "Registered"
            return render_template("register.html", message2 =msg)

    return render_template("register.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=False)