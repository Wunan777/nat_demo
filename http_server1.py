from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "<h1>Hello, World! I am local http server.</h1>"


if __name__ == "__main__":
    app.run(debug=True, port=8113)
