from flask import Flask

app = Flask(__name__)

@app.route('/')
def main():
    return "Come and find your nest"

if __name__=='__main__':
    app.run('0.0.0.0', debug="True")
