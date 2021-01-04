from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.model.criterion_has_tag import CriterionHasTag
from app.main.service.criterion_has_tag_service import CriterionHasTagService
from app.main.util import AlchemyEncoder
from app.main.util.dto import CriterionHasTagDto


api = CriterionHasTagDto.api
_criterion_has_tag = CriterionHasTagDto.criterion_has_tag


@api.route('/<public_id>')
@api.param('public_id', 'The CriterionHasTag identifier')
class CriterionHasTagInfo(Resource):
    @api.doc('get a criterion_has_tag')
    @api.marshal_with(_criterion_has_tag)
    def get(self, public_id):
        pid = public_id.split('-')
        data = {
            'criterion_id': pid[0],
            'tag_id': pid[1],
        }
        criterion_has_tag = CriterionHasTagService.get_a_criterion_has_tag(data)
        if not criterion_has_tag:
            api.abort(404, message="criterion_has_tag '{}' not found".format(public_id))
        else:
            return criterion_has_tag.as_dict()


@api.route('/info')
class AllCriterionHasTagsInfo(Resource):
    def get(self):
        criterion_has_tags = CriterionHasTagService.get_all(CriterionHasTag)
        try:
            if criterion_has_tags:
                body = [r.as_dict() for r in criterion_has_tags]
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
            api.abort(404, message="criterion_has_tag table not found or has no data")


@api.route('/create_criterion_has_tag')
class Create(Resource):
    @api.doc('create a new criterion_has_tag')
    def post(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        template = CriterionHasTag()
        allowed_keys = template.as_dict().keys()

        new_criterion_has_tag_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_criterion_has_tag_dict.update({key:data[key]})
        try:
            response = CriterionHasTagService.save_new_criterion_has_tag(new_criterion_has_tag_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/update_criterion_has_tag/<public_id>')
@api.param('public_id', 'The CriterionHasTag identifier')
class Update(Resource):
    @api.doc('update an existing criterion_has_tag')
    def put(self, public_id):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")

        #retrieve the criterion_has_tag to be updated
        pid = public_id.split('-')
        pid_data = {
            'criterion_id': pid[0],
            'tag_id': pid[1],
        }
        criterion_has_tag = CriterionHasTagService.get_a_criterion_has_tag(pid_data)
        if not criterion_has_tag:
            api.abort(404, message="criterion_has_tag '{}' not found".format(public_id))

        #set new key/values
        allowed_keys = criterion_has_tag.as_dict().keys()
        for key in data.keys():
            if key in allowed_keys:
                #DO NOT PREVENT PRIMARY KEY CHANGES
                setattr(criterion_has_tag, key, data[key])

        try:
            CriterionHasTagService.commit()
            return criterion_has_tag.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e


@api.route('/delete_criterion_has_tag/<public_id>')
@api.param('public_id', 'The CriterionHasTag identifier')
class Delete(Resource):
    @api.doc('delete a criterion_has_tag')
    def delete(self, public_id):
        pid = public_id.split('-')
        pid_data = {
            'criterion_id': pid[0],
            'tag_id': pid[1],
        }
        criterion_has_tag = CriterionHasTagService.get_a_criterion_has_tag(pid_data)
        if not criterion_has_tag:
            api.abort(404, message="criterion_has_tag '{}' not found".format(public_id))

        try:
            CriterionHasTagService.delete(criterion_has_tag)
            return criterion_has_tag.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
