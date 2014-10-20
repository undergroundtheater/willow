import logging
import sys
from flask.ext.script import Manager, Server
from willow.app import create_app

app = create_app()

manager = Manager(app)

if __name__ == '__main__':
    manager.run()
