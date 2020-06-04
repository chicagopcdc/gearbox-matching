from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
from time import gmtime, strftime
import json

from app.main.util.dto import StudyDto
from app.main.util import AlchemyEncoder
from app.main.service.study_service import get_all_studies, get_a_study, get_study_version

api = StudyDto.api
_study = StudyDto.study



@api.route('/<public_id>')
@api.param('public_id', 'The Study identifier')
@api.response(404, 'Study not found.')
class Study(Resource):
    @api.doc('get a study')
    @api.marshal_with(_study)
    def get(self, public_id):
        # return jsonify({"message": "Welcome to my Flask App"})

        study = get_a_study(public_id)

        print("PLUTOOOOOO")
        print(study.sites, flush=True)
        print(study.study_versions, flush=True)
        print(json.dumps([r.site.as_dict() for r in study.sites]), flush=True)

        if not study:
            api.abort(404)
        else:
            return study.as_dict()
        # return jsonify({
        #     "body": 
        # })

@api.route('/info')
class info(Resource):
    def get(self):
        studies = get_all_studies() # Study.query.all()

        # print("CIAOOOOOO", flush=True)
        # print(json.dumps(studies, cls=AlchemyEncoder))
        # print(json.dumps(a, cls=AlchemyEncoder), flush=True)
        #     print(a.as_dict(), flush=True)
        #     print(json.dumps(a.as_dict(), cls=AlchemyEncoder), flush=True)
        #     print(json.dumps(a.as_dict()), flush=True)

        print(json.dumps([r.as_dict() for r in studies]), flush=True)



        return jsonify({
            "current_date": date.today().strftime("%B %d, %Y"),
            "current_time": strftime("%H:%M:%S +0000", gmtime()),
            "status": "OK",
            "body": [r.as_dict() for r in studies]
        })

# @api.route('/study')
# class StudyList(Resource):
#     @api.doc('list_of_registered_studies')
#     @api.marshal_list_with(_study, envelope='data')
#     def get(self):
#         """List all registered users"""
#         return get_all_studies()

#     # @api.response(201, 'User successfully created.')
#     # @api.doc('create a new user')
#     # @api.expect(_user, validate=True)
#     # def post(self):
#     #     """Creates a new User """
#     #     data = request.json
#     #     return save_new_user(data=data)






# from typing import List, Dict
# import mysql.connector
# import json
# # from werkzeug import secure_filename
# from sqlalchemy import text
# # app.config["DEBUG"] = True
# # app.config["SQLALCHEMY_ECHO"] = True

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

#   # db.session.query("1").from_statement(text('SELECT 1')).all()
#   # try:
#   #   db.session.query("1").from_statement(text("SELECT 1")).all()
#   #   return '<h1>It works.</h1>'
#   # except:
#   #   return '<h1>Something is broken.</h1>'



# # @app.route('/blog/<int:postID>')
# # def show_blog(postID):
# #    return 'Blog Number %d' % postID

# # @app.route('/uploader', methods = ['GET', 'POST'])
# # def upload_file():
# #    if request.method == 'POST':
# #       f = request.files['file']
# #       f.save(secure_filename(f.filename))
# #       return 'file uploaded successfully'
