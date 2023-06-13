from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/')
def home():  # put application's code here
    return render_template("index.html")

@app.route('/right')
def right():
    return  render_template("right-sidebar.html")

@app.route('/left')
def left():
    return  render_template("left-sidebar.html")

@app.route('/no_sidebar')
def no_sidebar():
    return  render_template("no-sidebar.html")

if __name__ == '__main__':
    app.run(debug=True)
