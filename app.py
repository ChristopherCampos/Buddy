"""The main program file."""
from flask import Flask, request, abort, redirect, render_template, url_for, jsonify
from src.models import setup_db, User, Post
from flask_migrate import Migrate

TEMPLATE_FOLDER = "templates"


def create_app():
    """Creates the application with correct endpoints and error handlers"""
    app = Flask(__name__, template_folder=TEMPLATE_FOLDER)
    db = setup_db(app)
    migrate = Migrate(app, db)
    #db.create_all()

    """Endpoints"""
    @app.route("/")
    def default_route():
        return render_template("main_page.html", data=User.query.all())

    @app.route("/users/", methods=['GET', 'POST'])
    def users():
        if request.method == 'POST':
            body = request.get_json()
            if body is None:
                pass #abort error code
            new_username = body.get("username")
            if new_username:
                try:
                    new_user = User(username=new_username)
                except Exception:
                    pass


        elif request.method == 'GET':
            users = User.query.all()
            return " ".join([user.user_id for user in users])

    @app.route("/users/<int:user_id>")
    def retrieve_user(user_id):
        user = User.query.filter_by(user_id=user_id).one_or_none()
        if user is not None:
            return str(user_id)
        else:
            abort(404)

    """Error handlers"""
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422
    return app




if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run()
