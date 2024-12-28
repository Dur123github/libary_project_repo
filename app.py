from flask import Flask, jsonify, request,render_template, url_for, flash, session,redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
import bcrypt
from routes import UserRegistration,AddBook
from functools import wraps


app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/") 
db = client["libary_management"]  
collection = db["user_data"]
counter_collection = db['counters']
books_collection=db['book_collection']
add_book_manager = AddBook(books_collection, counter_collection)

app.secret_key=b'\x88\xa4\x8b[\x96lx\t\xf9=bK\xe6\xf6x\xac\xd2\xfa\xd8S\xf0;\xfb*'
CORS(app)
@app.route('/')
def index():
  # Redirect to the dashboard if logged in
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        user = collection.find_one({"username": username},{"_id": 0, "username": 1, "password": 1, "role": 1})

        if user:
            # Check if the password matches
          if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')) and user['role'] == role:
                session['username'] = user['username']
                session['role'] = user['role']
                flash("Login successful!", "success")
                return redirect(url_for('dashboard'))  # Redirect to the dashboard or another page
          else:
            # If credentials are invalid, flash an error and redirect to dashboard
            flash('Invalid username or password', 'danger')
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Remove session data
    session.pop('username', None)  # This will clear the session
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))
user_registration = UserRegistration(collection, counter_collection)
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
       if request.method == 'POST':
        form_data = request.form
        message, status_code = user_registration.validate_and_register(form_data)

        return message, status_code

       return render_template('register.html')






if __name__=="__main__":
    app.run(debug=True)
