import logging
from services.db_functions import get_last_month_gas_fees
from services.gas_functions import get_data_from_projects
from services.scrapping_functions import ADDRESSES
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from apscheduler.schedulers.background import BackgroundScheduler

#Parameters
USERNAME = "crypto_whale"
PASSWORD = "js*gnHfcx!"
try:
    logging.basicConfig(filename="Documentation/logs.txt", level=logging.INFO)
    app = Flask(__name__)
    app.config['DEBUG'] = False
    app.secret_key = 'fdjlhtlrehtwr0w834803wcjew'

    scheduler = BackgroundScheduler()
    scheduler.add_job(get_data_from_projects, 'interval', hours=1)
    scheduler.start()
except Exception as e:
    logging.critical('error in app.py: ' + str(e))

#Home route that redirects to login
@app.route('/')
def home():
    try:
        return redirect(url_for('login'))
    except Exception as e:
        logging.critical('Error in home function: ' + str(e))

#Login route for user authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
     try:
        if request.method == 'POST':
            session.pop('user', None)
            username = request.form['username']
            password = request.form['password']

            if username == USERNAME and password == PASSWORD:
                session['user'] = username
                return redirect(url_for('graph', project_name = 'Cryptopunks'))
            else:
                flash('Invalid username or password', 'error')

        return render_template('login.html')
     except Exception as e:
         logging.critical('Error in login function: ' + str(e))

#Graph route by the project name
@app.route('/graph/<string:project_name>')
def graph(project_name):
    try:
        if g.user:
            for project_data in ADDRESSES:
                if project_data[0] == project_name:
                    return render_template('chart.html', data=get_last_month_gas_fees(project_name),name=project_name, addresses = ADDRESSES)
            return redirect(url_for('error'))
        return render_template('unauthorized.html')
    except Exception as e:
        logging.critical('Error in graph function: ' + str(e))

#Logout route 
@app.route('/logout', methods=['GET','POST'])
def logout():
    try:
        session.pop('user', None)
        return redirect(url_for('login'))
    except Exception as e:
        logging.critical('Error in logout function: ' + str(e))

#Error routes

@app.route('/error')
def error():
    return render_template('error.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

if __name__ == '__main__':
    app.run(debug=True)