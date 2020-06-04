import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


from app import blueprint

from app.main import create_app, db
from app.main.model import study


app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')

app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run(host='0.0.0.0', debug=True)

@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()































# import pymysql

# from typing import List, Dict


# import mysql.connector
# import json

# from datetime import date
# from time import gmtime, strftime
# # from werkzeug import secure_filename

# from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import text

# from main.model.study import Study
# from main import create_app
# # from model.arm import Arm


# from main.service.study_service import get_all_studies

# app = create_app('dev')

# # app = Flask(__name__)
# # app.config["DEBUG"] = True
# # # # mysql+pymysql://user:password@/database?unix_socket=/cloudsql/project:us-central1:instance
# # app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:password@mysql-development:3306/pedal_dev_v_0"
# # app.config["SQLALCHEMY_ECHO"] = True
# # db = SQLAlchemy(app)

# # class Study(db.Model):
# #     """ User Model for storing user related details """
# #     __tablename__ = "study"

# #     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
# #     name = db.Column(db.String(45), nullable=True)
# #     code = db.Column(db.String(45), nullable=True)
# #     create_date = db.Column(db.DateTime, nullable=True)
# #     active = db.Column(db.Boolean, nullable=True)

# def favorite_colors() -> str: # List[Dict]:
#     config = {
#         'user': 'root',
#         'password': 'password',
#         'host': 'mysql-development',
#         'port': '3306',
#         'database': 'pedal_dev_v_0'
#     }
#     connection = mysql.connector.connect(**config)
#     cursor = connection.cursor()
#     cursor.execute('SELECT 1')
#     print(cursor, flush=True)
#     # results = [{name: color} for (name, color) in cursor]
#     results = ""
#     for name in cursor:
#       results += str(name) 
#     cursor.close()
#     connection.close()

#     return results


# @app.route('/')
# def index():
#   return jsonify({"message": "Welcome to my Flask App"})


# @app.route('/info')
# def info():
#   # return json.dumps({'favorite_colors': favorite_colors()})
#   # db.session.query("1").from_statement(text('SELECT 1')).all()
#   # try:
#   #   db.session.query("1").from_statement(text("SELECT 1")).all()
#   #   return '<h1>It works.</h1>'
#   # except:
#   #   return '<h1>Something is broken.</h1>'

#   studies = get_all_studies() # Study.query.all()

#   s = ""
#   for a in studies:
#     s = s + f'{a.id} {a.create_date}' + " "
#   return jsonify({
#     "current_date": date.today().strftime("%B %d, %Y"),
#     "current_time": strftime("%H:%M:%S +0000", gmtime()),
#     "status": "OK",
#     "body": s
#   })

# # @app.route('/blog/<int:postID>')
# # def show_blog(postID):
# #    return 'Blog Number %d' % postID

# # @app.route('/uploader', methods = ['GET', 'POST'])
# # def upload_file():
# #    if request.method == 'POST':
# #       f = request.files['file']
# #       f.save(secure_filename(f.filename))
# #       return 'file uploaded successfully'

# if __name__ == '__main__':
#   app.run(host='0.0.0.0', debug=True)
