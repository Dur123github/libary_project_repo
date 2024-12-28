# user_registration.py
import bcrypt
from functools import wraps

class UserRegistration:
    def __init__(self, db_collection,counter_collection):
        self.collection = db_collection
        self.counter_collection = counter_collection
    def get_next_counter(self):
        # Get the next unique id for user
        counter = self.counter_collection.find_one_and_update(
            {"_id": "user_id"},
            {"$inc": {"sequence_value": 1}},
            upsert=True,  # If the counter document does not exist, create it
            return_document=True  # Return the document after update
        )
        return counter["sequence_value"]
    def validate_and_register(self, form_data):
        # Extract data from the form
        name = form_data.get('name')
        email = form_data.get('email')
        username = form_data.get('username')
        phone = form_data.get('phone')
        password = form_data.get('password')
        confirm_password = form_data.get('confirmPass')
        gender = form_data.get('gender')
        role=form_data.get('role')

        if not all([name, email, username, phone, password, gender,role]):
            return "All fields are required!", 400

        # Check if passwords match
        if password != confirm_password:
            return "Passwords do not match!", 400
        if self.collection.find_one({"email": email}):
            return "This email is already registered!", 400

        if self.collection.find_one({"username": username}):
            return "This username is already taken!", 400

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        custom_id = self.get_next_counter()

        # Create a document to insert into MongoDB
        user_data = {
            "_id": custom_id,
            "fullname": name,
            "email": email,
            "username": username,
            "phone": phone,
            "password": hashed_password.decode('utf-8'),
            "gender": gender,
            "role":role
        }

        # Insert data into MongoDB
        self.collection.insert_one(user_data)

        return "Registration successful!", 200


class AddBook():
    def __init__(self, db_collection,counter_collection):
       self.db_collection=db_collection
       self.counter_collection=counter_collection

    def get_next_counter(self):
        # Get the next unique id for user
        counter = self.counter_collection.find_one_and_update(
            {"_id": "user_id"},
            {"$inc": {"sequence_value": 1}},
            upsert=True,  # If the counter document does not exist, create it
            return_document=True  # Return the document after update
        )
        return counter["sequence_value"] 
    
    def add_book_in_database(self, form_data,added_by):
        title=form_data.get('title')
        author=form_data.get('author')
        edition=form_data.get('edition')
        description=form_data.get('description')

        if not all([title, author, edition]):
            return "All fields are required!", 400
        book_id = self.get_next_counter_book()
        book = {
            "_id": book_id,
            "title": title,
            "author": author,
            "edition": edition,
            "description": description,
            "added_by": added_by  # Librarian's ID
        }

        # Insert the book into the database
        self.db_collection.insert_one(book)
        return "Book added successfully!", 201
        

        
       


    