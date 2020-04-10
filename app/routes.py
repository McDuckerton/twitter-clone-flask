from app import app
from flask import render_template, request, redirect, url_for, flash, abort, session
import os
from hashlib import sha1
#import mysql.connector

# HOST=os.environ['HOST']
# USER=os.environ['USERNAME']
# PASSWD=os.environ['PASSWD']
# DATABASE=os.environ['DATABASE']
# AUTH_DATABASE=os.environ['AUTH_DATABASE']

# def account_list():
#     db = mysql.connector.connect(
#         host = HOST,
#         user = session.get('username'),
#         passwd = session.get('password'),
#         database = DATABASE
#         )

#     dbcursor = db.cursor()
    
#     sql = ""
#     dbcursor.execute(sql)
#     response = dbcursor.fetchall()
#     response['THIS_KEY']

#     return ''

@app.route('/')
def home():
    # if not session.get('logged_in'):
    #     return render_template('login.html')
    # else:
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        if session.get('logged_in'):
            return redirect(url_for('index'))
        else:
            return render_template('login.html')
    else: 
        db = mysql.connector.connect(
            host = HOST,
            user = USER,
            passwd = PASSWD,
            database = AUTH_DATABASE
            )
        
        DB_USER = request.form['txt-username']
        DB_PASS = request.form['txt-password']
        
        dbcursor = db.cursor()
        
        SQL = f"select password from user where user=\'{DB_USER}\'"
        dbcursor.execute(SQL)
        
        HASH_RESPONSE = dbcursor.fetchall()
        HASHED_PASS = HASH_RESPONSE[0][0]
        NEW_HASHED_PASS = (HASHED_PASS.decode('utf-8'))
        COMP_PASS = "*" + sha1(sha1(str.encode(DB_PASS)).digest()).hexdigest().upper()

        if NEW_HASHED_PASS == COMP_PASS: 
            session['logged_in'] = True
            session['username'] = request.form['txt-username']
            session['password'] = request.form['txt-password']
            return redirect(url_for('index'))
        else:
            session['logged_in'] = False
            return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        session['logged_in'] = False
        session.pop('username', None)
        session.pop('password', None)
        return render_template('logout.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    return render_template('signup.html')

@app.route('/index', methods=['GET','POST'])
def index():
    # if not session.get('logged_in'):
    #     return redirect(url_for('login'))
    # else:
    return render_template('index.html')

@app.route('/getpassword', methods=['POST','GET'])
def get_password():
    
    if not session.get('logged_in') or method == 'GET':     
        return redirect(url_for('login'))
    else:    
        db = mysql.connector.connect(
            host = HOST,
            user = session.get('username'),
            passwd = session.get('password'),
            database = DATABASE
            )
    
        dbcursor = db.cursor()
        
        acct_name = request.form['dropdown']

        sql = "select password from c2s_accounts where cap_acct_name=\'%s\'" % acct_name
        dbcursor.execute(sql)
        response = dbcursor.fetchall()
        password = response[0][0]

        name_list,num_list = account_list() 
        return render_template('index.html',get_pass=password,c2s_accounts=zip(name_list,num_list),get_password=zip(name_list,num_list))

@app.route('/changepassword', methods=['POST','GET'])
def change_password():
    
    if not session.get('logged_in') or method == 'GET':
        return redirect(url_for('login'))
    else:
        db = mysql.connector.connect(
            host = HOST,
            user = session.get('username'),
            passwd = session.get('password'),
            database = DATABASE
            )

        dbcursor = db.cursor()
        
        change_pass = request.form['txt_change_pass']
        acct_name = request.form['dropdown']

        sql = "update c2s_accounts set password=%s where cap_acct_name=%s"
        val = (change_pass, acct_name)
        dbcursor.execute(sql,val)
        db.commit()
        name_list,num_list = account_list()
        return render_template('index.html', c2s_accounts=zip(name_list,num_list),get_password=zip(name_list,num_list))
        

@app.route('/addaccount', methods=['POST','GET'])
def add_account():
    
    if not session.get('logged_in') or method == 'GET':
        return redirect(url_for('login'))
    else:
        db = mysql.connector.connect(
            host = HOST,
            user = session.get('username'),
            passwd = session.get('password'),
            database = DATABASE
            )
        
        dbcursor = db.cursor()

        new_acct_name = request.form['txt_add_acct_name']
        new_acct_num = request.form['txt_add_acct_num']
        new_acct_pass = request.form['txt_add_pass']
        
        sql = "insert into c2s_accounts (cap_acct_name,acct_num,password) " + "values (%s,%s,%s)"
        val = (new_acct_name,new_acct_num,new_acct_pass)
        dbcursor.execute(sql,val)
        db.commit()
        name_list,num_list = account_list()
        return render_template('index.html', c2s_accounts=zip(name_list,num_list),get_password=zip(name_list,num_list))