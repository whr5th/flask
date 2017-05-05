from flask import Flask, render_template 
import requests

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('homepage.html')

@app.route('/hello/<name>')
def hello(name):
  return render_template('name.html', name=name)

@app.route('/<command>')
def command(command):
	return render_template('command.html', command=command)

@app.route('/image')
def analyze():
	return render_template('image.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
