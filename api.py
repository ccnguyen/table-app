import time
from flask import Flask
# from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='build', static_url_path='/')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/template1'
# db = SQLAlchemy(app)

@app.route('/')
def index():
	return app.send_static_file('index.html')

@app.route('/api/time')
def get_current_time():
	return {'time': time.time()}
