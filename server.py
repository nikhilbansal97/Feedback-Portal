from flask import Flask, render_template, url_for, request, redirect
import random, string
from flask import session as lSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Form, User, Base
# For signin
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

engine = create_engine('sqlite:///formdatabase.db')
Base.metadata.bind = engine

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
@app.route('/form/new')
def displayForm():
    username = ""
    if 'access_token' not in lSession or lSession['access_token'] is None:
        username = "None"
        login = 0
    else:
        username = lSession['username']
        login = 1
    return render_template('index.html', edit=0, login=login, username=username)

@app.route('/login')
def login():
    if 'access_token' not in lSession or lSession['access_token'] is None:
        state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                        for x in range(32))
        # Save the random state generated in the lSession.
        lSession['state'] = state
        return render_template('login.html', STATE=state)
    return redirect(url_for('showAllForms'))

@app.route('/gdisconnect')
def gdisconnect():
    # Check if the user is already logged out.
    if 'access_token' not in lSession or lSession['access_token'] is None:
        return redirect(url_for('showMovies'))
    access_token = lSession.get('access_token')
    if access_token is None:
        response = make_response('Currect user not connected.', 401)
        response.headers['Content-Type'] = "application/json"
        return response
    # Revoke the access token given by  Google OAuth.
    url = "https://accounts.google.com/o/oauth2/revoke?token=%s" % access_token
    h = httplib2.Http()
    resp, content = h.request(url, 'GET')
    print(content)
    print(resp.get('status'))
    print("Logged out!")
    lSession['state'] = None
    lSession['access_token'] = None
    return redirect(url_for('displayForm'))

@app.route('/forms')
def showAllForms():
    if 'access_token' not in lSession or lSession['access_token'] is None:
        return redirect(url_for('gconnect'))
    forms = session.query(Form).all()
    if len(forms) == 0:
        print("Forms Database empty");
    return render_template('formsList.html',forms=forms)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Check if the connection is established and is secure
    if request.args.get('state') != lSession['state']:
        response = make_response(json.dumps('Invalid State Parameter'), 401)
        response.headers['Content-Type'] = "application/json"
        return response
    code = request.data
    try:
        # Upgrade the authorization code to credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope="")
        oauth_flow.redirect_uri = "postmessage"
        # Exchange the one time code with Google OAuth to get the credentials
        # object.
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps(
            'Failed to upgrade the authorization code.', 401))
        response.headers['Content-Type'] = "application/json"
        return response
    # Check that the acess token is valid
    access_token = credentials.access_token
    url = ("https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s" %
           access_token)
    h = httplib2.Http()
    resp, content = h.request(url, 'GET')
    result = json.loads(content.decode('utf-8'))

    # If there was an error in access token, abort.
    if 'error' in result:
        response = make_request(json.dumps(
            "Token's user ID doesn't match the given user id"), 401)
        response.headers['Content-Type'] = "application/json"
        return response
    # Verify that the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps(
            "Token's user ID doesn't match the user id"), 401)
        response.headers['Content-Type'] = "application/json"
        return response
    # Check if user is already logged in.
    stored_credentials = lSession.get('access_token')
    stored_gplus_id = lSession.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps("User is already logged in"), 200)
        response.headers['Content-Type'] = "application/json"
        return response
    # Store the acess token in the login session for later use
    lSession['access_token'] = credentials.access_token
    lSession['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    lSession['username'] = data["name"]
    lSession['picture'] = data["picture"]
    lSession['email'] = data["email"]

    # userInfo = session.query(User).filter_by(email=data["email"]).one_or_none()
    # # If a new user is logged in, then generate an random api key and add it
    # # to the Users table.
    # if userInfo is None:
    #     newUser = User(name=data["name"], email=data[
    #                    "email"], api_key=getRandomToken())
    #     session.add(newUser)
    #     session.commit()

    output = ''
    output += '<h1>Welcome, '
    output += lSession['username']
    output += '!</h1>'
    output += '<img src="'
    output += lSession['picture']
    output += ' " style="width:300px;height:300px;'
    output += 'border-radius:150px;-webkit-border-radius:150px;'
    output += '-moz-border-radius:150px;"> '
    print("done!")
    return output


@app.route('/edit/<int:id>/<int:edit>', methods=['POST'])
def editForm(id, edit):
    print (id, edit)
    if 'access_token' not in lSession or lSession['access_token'] is None:
        login = 0
        username = "None"
        return render_template('index.html', form=None, edit=0, login=login, username=username)
    else:
        login = 1
        username = lSession['username']
        form = session.query(Form).filter_by(id=id).one_or_none()
        if edit == 1:
            form.first_name = request.form['first_name']
            form.last_name = request.form['last_name']
            form.food = request.form['food']
            form.email = request.form['email']
            form.roll = request.form['roll']
            form.accomodation = request.form['accomodation']
            form.cleanliness = request.form['cleanliness']
            form.complain = request.form['complain']
            form.behaviour = request.form['behaviour']
            form.medical = request.form['medical']
            session.add(form)
            session.commit()
            print ("updated!!")
            return redirect(url_for('displayForm'))
        else:
            return render_template('index.html', form=form, edit=1, login=login, username=username)


@app.route('/delete/<int:id>', methods=['POST'])
def deleteForm(id):
    if 'access_token' not in lSession or lSession['access_token'] is None:
        print ("User not logged in")
        return redirect(url_for('displayForm'))
    form = session.query(Form).filter_by(id=id).one_or_none()
    session.delete(form)
    session.commit()
    return redirect(url_for('showAllForms'))

@app.route('/insertData', methods=['POST'])
def insertFormData():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    food = request.form['food']
    email = request.form['email']
    roll = request.form['roll']
    accomodation = request.form['accomodation']
    cleanliness = request.form['cleanliness']
    complain = request.form['complain']
    behaviour = request.form['behaviour']
    medical = request.form['medical']
    form = Form(first_name = first_name, last_name = last_name, food=food, email_id=email, roll=roll, accomodation=accomodation, clean=cleanliness,complain=complain, behaviour=behaviour, medical=medical)
    session.add(form)
    session.commit()
    print("Data Added!")
    if 'access_token' not in lSession or lSession['access_token'] is None:
        return redirect(url_for('displayForm'))
    return redirect(url_for('showAllForms'))

if __name__ == "__main__":
    app.secret_key = "secret_key"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
