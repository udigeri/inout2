import argparse

from inout2.web import WebApp
from inout2.app import App
from flask import render_template


inout2 = WebApp(debug=True)
flask_app = inout2.flask



@flask_app.route("/")
def view_home():
    return render_template("welcome.jinja")

@flask_app.route("/login/")
def view_login():
    return render_template("login.jinja")

@flask_app.route("/admin/")
def view_admin():
    return render_template("admin.jinja")

@flask_app.route("/about/")
def view_about():
    return render_template("about.jinja")



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
    parser.add_argument('-p', '--port', dest='web_port',
                                action='store',
                                default="80",
                                help='Define web server port (default: %(default)s)')

    app = App(__version__, parser.parse_args())
    app.run(inout2)
    app.finished()
    