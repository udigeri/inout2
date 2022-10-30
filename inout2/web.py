# # import os
from flask import Flask
import requests
from requests.auth import HTTPBasicAuth

class WebApp():
    HOST = "0.0.0.0"
    PORT = 80
    DEBUG = False
    SECRET_KEY = 'my_uno-tuti_secret_things2'

    def __init__(self, host=HOST, port=PORT, debug=DEBUG):
        self.host = host
        self.port = port
        self.debug = debug
        self.flask = Flask(__name__)
        self.flask.config.from_object(self)


    def run(self, config, logger):
        self.config = config
        self.logger = logger
        # self.pgs = Pgs(self.config, self.logger)
        self.port = getattr(self.config, "web_port")
        logger.info(f"Web module started on {self.host} :{self.port} debug {self.debug}")

        # http
        self.flask.run(host=self.host, port=self.port, debug=self.debug)

        # https
        # self.flask.run(host=self.host, port=self.port, debug=self.debug, ssl_context='adhoc')

    def _getAuthenticationURL(self):
        return self.pgs._getHost() #+ "/pgs"

    def getAuthentication(self, usr, pwd):
        self.username = usr
        self.password = pwd

        error = None
        self.pgs.setAuth(HTTPBasicAuth(usr, pwd))
        try:
            rsp = requests.get(self._getAuthenticationURL(), auth=HTTPBasicAuth(usr, pwd))
            if rsp.status_code != 404 and rsp.status_code != 200:
                error = "Authentication failed Status code {} {}".format(rsp.status_code, self._getAuthenticationURL())
                self.logger.warning(error)
            else:
                self.logger.info("Web Authentication success on {}".format(self._getAuthenticationURL()))
        except Exception as err:
            error = "Authentication failed {}".format(err)
            self.logger.error(error)
        return error
