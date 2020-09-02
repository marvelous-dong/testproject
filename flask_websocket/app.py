from flask import Flask, render_template
from flask_cors import CORS
from database import configs

app = Flask(__name__)

app.config['DEBUG'] = True

CORS(app, supports_credentials=True)
# app.config.from_object(configs)


@app.route("/toy")
def toy():
    return render_template("toy.html")


if __name__ == '__main__':
    app.run(port=9527)

