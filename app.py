"""The main program file."""
from flask import Flask, request, abort, redirect, render_template, url_for
from src.models import setup_db, User, Post
from flask_migrate import Migrate

TEMPLATE_FOLDER = "templates"


def create_app():
    app = Flask(__name__, template_folder=TEMPLATE_FOLDER)
    db = setup_db(app)
    migrate = Migrate(app, db)

    @app.route("/")
    def default_route():
        return render_template("main_page.html", data=User.query.all())

    @app.route("/users/")
    def retrieve_users():
        users = User.query.all()
        return " ".join([user.user_id for user in users])

    @app.route("/users/<int:user_id>")
    def retrieve_user(user_id):
        user = User.query.filter_by(user_id=user_id).one_or_none()
        if user is not None:
            return str(user_id)
        else:
            abort(404)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
