from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your secret key"


mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'T0nylhs#9999'
app.config['MYSQL_DB'] = 'smashdojo'

mysql.init_app(app)


@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', username=session["username"])
    else:
        return render_template('index.html')
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)

        # Store the user in the database
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (email, username, password) VALUES (%s, %s, %s)',
                        (email, username, hashed_password))
        conn.commit()
        cursor.close()
        return redirect('/homepage')

    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user[3], password):
            session['username'] = user[2]
            return redirect(url_for('homepage', username=user[2]))
        else:
            return 'Invalid email or password'
    
    return render_template('signin.html')
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/homepage/<username>')
def homepage(username):
    return render_template('homepage.html', username=username)

@app.route('/matchmaking')
def matchmaking():
    return render_template('matchmaking.html')

if __name__ == '__main__':
    app.run(debug=True)