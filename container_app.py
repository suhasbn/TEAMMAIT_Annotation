from flask import Flask, render_template, request, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import prodigy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this!
login_manager = LoginManager(app)

# Mock user database (replace with actual database later)
users = {'doctor1': {'password': generate_password_hash('password1')},
         'doctor2': {'password': generate_password_hash('password2')}}

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username]['password'], password):
            user = User()
            user.id = username
            login_user(user)
            return jsonify({"success": True})
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"success": True})

@app.route('/')
@login_required
def index():
    # Start Prodigy session here
    return prodigy.serve('audio_annotation', 'your-s3-bucket-name')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
