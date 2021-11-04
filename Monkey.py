#to import environment run . environment.sh sets the app name and environment for flask. 
from flask import Flask, render_template, url_for,request, flash, redirect
from markupsafe import escape
import re
import sqlite3
from werkzeug.exceptions import abort
import geolocation
import textExchange

app = Flask(__name__) 

@app.route('/', methods =["GET", "POST"])
def index():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        mood = request.form.get("moods")
        country = request.form.get("places")
        # getting input with name = lname in HTML form
        #last_name = request.form.get("lname")

        print("Mood Selected " + mood + " Country Selected " + country, "\n")
        print(geolocation.GetCoordinates('North America'))

    return render_template('index.html')

#use render template to call 
#def index():
#    return render_template('index.html')


@app.route('/You_Did_it')
def Monkeysite():
    return render_template('You_did_it.html')

#add additional route
@app.route('/contact', methods =["GET", "POST"])
def contact():
    """
    if request.method == "POST":
        # getting input with name = fname in HTML form
        mood = request.form.get("moods")
        # getting input with name = lname in HTML form
        #last_name = request.form.get("lname")
        return "Mood Selected " + mood
    return render_template('contact.html')
    """
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        content = request.form['content']
        if not name:
            flash('Name is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO contacts (uname, email, content) VALUES (?, ?, ?)',
                         (name, email, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('contact.html')


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % escape(username)


#print out the urls for the functions 
with app.test_request_context():
    print('URL for index: ',url_for('index'))
    print('URL for contact: ',url_for('contact'))
    print(url_for('Monkeysite'))
    print(url_for('show_user_profile', username = 'George'))
    #HTML_editor('index.html')

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_contacts(contacts_id):
    conn = get_db_connection()
    contacts = conn.execute('SELECT * FROM contacts WHERE id = ?',
                        (contacts_id,)).fetchone()
    conn.close()
    if contacts is None:
        abort(404)
    return contacts
    
if __name__ == "__main__":
    app.run(debug=True)