from flask import Flask

app = Flask(__name__)

@app.route('/')
def main():
    return("Come and find your nest")
