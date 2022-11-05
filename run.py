import argparse

from inout2.web import WebApp
from inout2.app import App
from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from flask import session
from flask import flash
from flask import g

import sqlite3

inout2 = WebApp(debug=True)
flask_app = inout2.flask



@flask_app.route("/")
def view_home():
    return render_template("welcome.jinja")



@flask_app.route("/login/", methods=["GET"])
def view_login():
    return render_template("login.jinja")



@flask_app.route("/login/", methods=["POST"])
def login_user():
    """Create session when correct user/password provided"""
    username = request.form['username']
    password = request.form['password']
    if username == "testexport" and password == "testexport":
        session["logged"] = True
        return redirect(url_for("view_admin"))
    else:
        return redirect(url_for("view_login"))



@flask_app.route("/logout/", methods=["GET", "POST"])
def logout_user():
    """Drop session"""
    session.pop("logged")
    return redirect(url_for("view_home"))



@flask_app.route("/admin/")
def view_admin():
    return render_template("admin.jinja")



@flask_app.route("/about/")
def view_about():
    return render_template("about.jinja")



## UTILS
def connect_db():
    rv = sqlite3.connect(inout2.DATABASE)
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@flask_app.teardown_appcontext
def close_db(error):
    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()



def init_db(app):
    with app.app_context():
        db = get_db()
        with open("inout2/schema.sql", "r") as fp:
            db.cursor().executescript(fp.read())
        db.commit()




if (__name__ == "__main__"):
    __version_info__ = ('0','1','0')
    __version__ = '.'.join(__version_info__)

    parser = argparse.ArgumentParser(prog="InOut2",
                                        description='InOut2 Parking lot web',
                                        epilog='Pavol Hudák')
    parser.add_argument('-v', '--version', action='version',
                                version='%(prog)s ('+__version__+')')
    parser.add_argument('-c', '--config', dest='config_file_path',
                                action='store',
                                default="./inout2/config.yml",
                                help='Path to config file (default: %(default)s)')
    parser.add_argument('-e', '--env', dest='config_env',
                                action='store',
                                default="production",
                                help='Define conguration environment (default: %(default)s)')
    parser.add_argument('-i', '--init', dest='init_db',
                                action='store',
                                required=False,
                                help='Init database')



    app = App(__version__, parser.parse_args())
    if (app.config.params.init_db != None):
        init_db(inout2.flask)
        app.logger.info("Initialize DB finished")

    else:
        app.run(inout2)
        app.finished()
