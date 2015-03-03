import logging
import sys
from flask.ext.assets import ManageAssets
from flask.ext.migrate import MigrateCommand
from flask.ext.script import Manager, Server
from willow.app import create_app

app = create_app()

manager = Manager(app)
manager.add_command('assets', ManageAssets)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
