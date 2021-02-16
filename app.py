from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
import pymongo
from bson.objectid import ObjectId


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'



app = Flask(__name__)
app.secret_key = 'user@123'

#connect with mongoDB

client = pymongo.MongoClient("mongodb+srv://user:user123@cluster0.33dbn.mongodb.net/users?retryWrites=true&w=majority")
db = client.users
mycol = db["users"]

users = (mycol.find_one({'_id' : ObjectId('602b91c6a4426b1f8ccad14a')}))

print("nasd" + str(users))
# users.append(User(id=1, username='Anthony', password='password'))
# users.append(User(id=2, username='Becca', password='secret'))
# users.append(User(id=3, username='Carlos', password='somethingsimple'))



@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        users = (mycol.find_one({'_id': ObjectId(session['user_id'])}))
        if users is not None:
            print(users['username'])
            g.user = users['username']
        # user = [x for x in users if x["_id"] == session['user_id']][0]
        # g.user = user
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']

        users = (mycol.find_one({"username": username, "password": password}))
        print('Users:' + str(users))

        if users is not None:
            password = users['password']
            user = username
            if user and users['password'] == password:
                session['user_id'] = str(users['_id'])
                return redirect(url_for('profile'))

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')


@app.route('/')
def index():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('index.html')


@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.clear()

    return render_template('index.html')