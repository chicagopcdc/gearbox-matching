from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.model.study_links import StudyLinks
from app.main.service.study_links_service import StudyLinksService
from app.main.util import AlchemyEncoder
from app.main.util.dto import StudyLinksDto


api = StudyLinksDto.api
_study_links = StudyLinksDto.study_links


@api.route('/<public_id>')
@api.param('public_id', 'The Study identifier')
class StudyLinksInfo(Resource):
    @api.doc('get a study_links')
    @api.marshal_with(_study_links)
    def get(self, public_id):
        study = StudyLinksService.get_a_study_links(self, public_id)
        if not study:
            api.abort(404, message="study '{}' not found".format(public_id))
        else:
            return study.as_dict()


@api.route('/info')
class AllStudyLinkssInfo(Resource):
    def get(self):
        study_linkss = StudyLinksService.get_all(StudyLinks)
        try:
            if study_linkss:
                body = [r.as_dict() for r in study_linkss]
            else:
                body = []
            return jsonify(
                {
                    "current_date": date.today().strftime("%B %d, %Y"),
                    "current_time": strftime("%H:%M:%S +0000", gmtime()),
                    "status": "OK",
                    "body": body
                }
            )
        except:
            api.abort(404, message="study_links table not found or has no data")


@api.route('/create_study_links')
class Create(Resource):
    @api.doc('create a new study_links')
    def post(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        template = StudyLinks()
        allowed_keys = template.as_dict().keys()

        new_study_links_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_study_links_dict.update({key:data[key]})
        try:
            response = StudyLinksService.save_new_study_links(StudyLinksService, new_study_links_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/update_study_links/<public_id>')
@api.param('public_id', 'The StudyLinks identifier')
class Update(Resource):
    @api.doc('update an existing study_links')
    def put(self, public_id):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")

        #retrieve the study_links to be updated
        study_links = StudyLinksService.get_a_study_links(self, public_id)
        if not study_links:
            api.abort(404, message="study_links '{}' not found".format(public_id))

        #set new key/values
        allowed_keys = study_links.as_dict().keys()
        for key in data.keys():
            if key in allowed_keys:
                setattr(study_links, key, data[key])
        try:
            StudyLinksService.commit()
            return study_links.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e


@api.route('/delete_study_links/<public_id>')
@api.param('public_id', 'The StudyLinks identifier')
class Delete(Resource):
    @api.doc('delete a study_links')
    def delete(self, public_id):
        study_links = StudyLinksService.get_a_study_links(self, public_id)
        if not study_links:
            api.abort(404, message="study_links '{}' not found".format(public_id))

        try:
            StudyLinksService.delete(study_links)
            return study_links.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
