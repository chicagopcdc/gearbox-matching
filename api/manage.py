import os
import subprocess
import sys
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import blueprint
from app.main import create_app, DbSession
from app.main.model import study


config_name = os.getenv('BOILERPLATE_ENV') or 'dev'
app = create_app(config_name, config_name)

app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, DbSession)

manager.add_command('DbSession', MigrateCommand)

@manager.command
def run():
    app.run(host='0.0.0.0', debug=True)

@manager.command
def test():
    """
    Runs pytest, which also runs unittests.
    Use pytest for DB operations, unittest for other code.
    """
    status = subprocess.call("pytest", shell=True)
    sys.exit(status)

if __name__ == '__main__':
    manager.run()
