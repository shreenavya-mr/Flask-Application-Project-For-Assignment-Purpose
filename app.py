from flask import Flask, render_template, request, redirect, url_for, session
import config

app = Flask(__name__)
app.secret_key = "supersecretkey"   # just for sessions
app.url_map.strict_slashes = False

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return redirect(url_for('home'))

    username = (request.form.get('username') or '').strip()
    password = (request.form.get('password') or '').strip()

    if username == config.SECRET_USERNAME and password == config.SECRET_PASSWORD:
        session['user'] = username
        return redirect(url_for('dashboard'))
    else:
        return render_template('result.html', success=False, user=username)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template('dashboard.html', 
                           user=session['user'],
                           api_key=config.API_KEY,
                           db_password=config.DB_PASSWORD,
                           server_ip=config.SERVER_IP)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
