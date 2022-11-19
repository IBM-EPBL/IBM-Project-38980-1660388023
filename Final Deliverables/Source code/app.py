from flask import Flask, request, render_template, redirect, url_for
from detect import start_test
#loading the model

from cloudant.client import Cloudant

#Authenticate using an IAM API key
client = Cloudant.iam('a1885fb9-67af-469a-83e5-f1f78af7b19a-bluemix','dBqnX2HXtY8Dxm6Gd8nWvmiQ5R-f4HaM_seOK96b30zj', connect=True)

#Create a database using an initialized client
my_database = client.create_database('my_database')

app=Flask(__name__)

#default home page or route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

#registration page
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/afterreg', methods=['POST'])
def afterreg():
    x = [x for x in request.form.values()]
    print(x)
    data = {
    'email': x[1], #Setting _id is optional
    'fullname': x[0],
    'password': x[2]
    }
    print(data)

    query = {'email': {'$eq': data['email']}}

    docs = my_database.get_query_result(query)
    print(docs)

    print(len(docs.all()))
    
    if(len(docs.all())==0):
        url = my_database.create_document(data)
        #response = requests.get(url)
        return render_template('register.html', pred="Registration Successful, please login using your details")
    else:
        return render_template('register.html', pred="You are already a member,please login using your details")

#login page
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/afterlogin',methods=['POST'])
def afterlogin():
    user = request.form['email']   
    passw = request.form['password']
    print(user,passw)

    query = {'email': {'$eq': user}} 

    docs = my_database.get_query_result(query)
    print(docs)

    print(len(docs.all()))

    if(len(docs.all())==0):
        return render_template('login.html', pred="The username is not found.")
    else:
        if((user==docs[0][0]['email'] and passw==docs[0][0]['password'])):
            return redirect('/prediction')
        else:
           return render_template('login.html',pred="Invalid user")
#prediction page
@app.route('/prediction')
def prediction():
    return render_template('prediction.html')

#logout page
@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/start', methods=['POST'])
def start():
    start_test()
    return redirect('/prediction')


if __name__=='__main__':
    app.run(debug=True)



