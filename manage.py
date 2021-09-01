#!/usr/local/bin/python3

import os
import unittest

# from flask_script import Manager
from api import blueprint
from api.main import create_app

app = create_app('dev')
app.register_blueprint(blueprint)

# manager = Manager(app)


# @manager.command
# def run():
#     app.run()


if __name__ == '__main__':
    if app.debug:
        app.run(host="0.0.0.0")
    else:
        app.run(host="0.0.0.0", port=5000, ssl_contex=('cert.pem', 'key.pem'))
