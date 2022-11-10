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

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import InputRequired

from inout2.models import db
from inout2.models import Users
from inout2.models import Tenant



inout2 = WebApp(debug=True)
flask_app = inout2.flask

## INIT DATABASE
db.init_app(flask_app)

##FORMS

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])



##CONTROLLERS

@flask_app.route("/")
def view_home():
    return render_template("welcome.jinja")



@flask_app.route("/login/", methods=["GET"])
def view_login():
    login_form = LoginForm()
    return render_template("login.jinja", form=login_form)



@flask_app.route("/login/", methods=["POST"])
def login_user():
    """Create session when correct user/password provided"""
    login_form = LoginForm(request.form)
    if login_form.validate():
        if login_form.username.data == "testexport" and \
            login_form.password.data == "testexport":
            session["logged"] = True
            flash("Login successfull")
            return redirect(url_for("view_admin"))
        else:
            flash("Invalid credentials", "alert")
            return redirect(url_for("view_login"))
    else:
        for error in login_form.errors:
            flash("{} is missing".format(error), "alert")
        return redirect(url_for("view_home"))



@flask_app.route("/logout/", methods=["GET", "POST"])
def logout_user():
    """Drop session"""
    session.pop("logged")
    flash("Successfully Logouted")
    return redirect(url_for("view_home"))



@flask_app.route("/tenants/")
def view_tenants():
    if "logged" in session:
        tenants = Tenant.query.order_by(Tenant.ten_id.desc())
        return render_template("tenants.jinja", tenants=tenants)
    else:
        flash("You must be Logged", "alert")
        return render_template("welcome.jinja")



@flask_app.route("/users/")
def view_users():
    if "logged" in session:
        users = Users.query.order_by(Users.id.desc())
        tenant = Tenant.query.order_by(Tenant.ten_id.desc())
        return render_template("users.jinja", users=users, tenants=tenant)
    else:
        flash("You must be Logged", "alert")
        return render_template("welcome.jinja")



@flask_app.route("/adduser/")
def add_user():
    if "logged" in session:
        new_user = Users(
            id = "1",
            name = "Pavol",
            username = "Udi",
            password = "PavolPwd")
        db.session.add(new_user)
        db.session.commit()
        users = Users.query.order_by(Users.id.desc())
        return render_template("users.jinja", users=users)



@flask_app.route("/admin/")
def view_admin():
    return render_template("admin.jinja")



@flask_app.route("/about/")
def view_about():
    return render_template("about.jinja")



## CLI COMMAND

def init_db(app):
    with app.app_context():
        db.create_all()



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
        init_db(flask_app)
        app.logger.info("Initialize DB finished")

    else:
        app.run(inout2)
        app.finished()
