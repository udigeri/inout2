# # import os
from flask import Flask

class WebApp():
    HOST = "0.0.0.0"
    PORT = 80
    DEBUG = False
    SECRET_KEY = 'my_uno-tuti_secret_things2'
    # DATABASE = "inout2/inout2.db"
    #SQLALCHEMY_DATABASE_URI = "sqlite:///../inout2/inout2.db"
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost:5432/pgs_standard"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

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
        logger.info(f"Web module started on {self.host}:{self.port} debug {self.debug}")

        # http
        self.flask.run(host=self.host, port=self.port, debug=self.debug)

        # https
        # self.flask.run(host=self.host, port=self.port, debug=self.debug, ssl_context='adhoc')
