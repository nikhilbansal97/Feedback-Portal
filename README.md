# Feedback Portal

This is a Hostel Heedback portal that contains a form to submit and the admin can edit and delete the forms submitted.

## Python Modules Required
* Flask
* Sqlalchemy
* oauth2client
* httplib2
* json
* requests

## Instructions:

1. Download python and pip from the official website.

2. Install all the pip modules mentioned above.
	
	**Windows (open `cmd`):**
	> pip install -r requirements.txt

	**Linux (open `terminal`):**
	> sudo pip install -r requirements.txt

3. Run the `database_setup.py` file to create the schema of database.

4. Run the `populateDatabase.py` file to add sample enteries in the database.

5. Run `server.py`file to run the server. You can access the server at:
	> localhost:5000

The default page will show the form to submit the feedback.

The `CONSOLE` button will work if you login using the ADMIN account. 

**To set your credentials as admin:**
	The `server.py` file contains variables `ADMIN_USERNAME` and `ADMIN_EMAIL`. You can change it to be yours and restart the server.