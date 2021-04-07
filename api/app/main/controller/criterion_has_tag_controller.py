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


@api.route('')
class CriterionHasTagInfo(Resource):
    @api.doc('get a criterion_has_tag')
    @api.marshal_with(_criterion_has_tag)
    def get(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        criterion_has_tag = CriterionHasTagService.get_a_criterion_has_tag(self, data)
        if not criterion_has_tag:
            api.abort(404, message="criterion_has_tag '{}' not found".format(data))
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
            response = CriterionHasTagService.save_new_criterion_has_tag(CriterionHasTagService, new_criterion_has_tag_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/delete_criterion_has_tag')
class Delete(Resource):
    @api.doc('delete a criterion_has_tag')
    def delete(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        criterion_has_tag = CriterionHasTagService.get_a_criterion_has_tag(self, data)
        if not criterion_has_tag:
            api.abort(404, message="criterion_has_tag '{}' not found".format(data))

        try:
            CriterionHasTagService.delete(criterion_has_tag)
            return criterion_has_tag.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
