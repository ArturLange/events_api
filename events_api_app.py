from flask import Flask

from database import db
from settings import SQLALCHEMY_DATABASE_URI
from views import add_routes


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app


app = create_app()


if __name__ == "__main__":
    add_routes(app)
    app.run(debug=True)
