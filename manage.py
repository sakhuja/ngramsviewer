from flask.ext.script import Manager
from processor import main_app

# By default, Flask-Script adds the 'runserver' and 'shell' commands to
# interact with the Flask application. Add additional commands using the
# `@manager.command` decorator, where Flask-Script will create help
# documentation using the function's docstring. Try it, and call `python
# manage.py -h` to see the outcome.

manager = Manager(main_app)

if __name__ == '__main__':
    manager.run()
