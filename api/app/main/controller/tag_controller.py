from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.model.tag import Tag
from app.main.service.tag_service import TagService
from app.main.util import AlchemyEncoder
from app.main.util.dto import TagDto


api = TagDto.api
_tag = TagDto.tag


@api.route('/<public_id>')
@api.param('public_id', 'The Tag identifier')
class TagInfo(Resource):
    @api.doc('get a tag')
    @api.marshal_with(_tag)
    def get(self, public_id):
        tag = TagService.get_a_tag(self, public_id)
        if not tag:
            api.abort(404, message="tag '{}' not found".format(public_id))
        else:
            return tag.as_dict()


@api.route('/info')
class AllTagsInfo(Resource):
    def get(self):
        tags = TagService.get_all(Tag)
        try:
            if tags:
                body = [r.as_dict() for r in tags]
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
            api.abort(404, message="tag table not found or has no data")


@api.route('/create_tag')
class Create(Resource):
    @api.doc('create a new tag')
    def post(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        template = Tag()
        allowed_keys = template.as_dict().keys()

        new_tag_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_tag_dict.update({key:data[key]})
        try:
            response = TagService.save_new_tag(TagService, new_tag_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/update_tag/<public_id>')
@api.param('public_id', 'The Tag identifier')
class Update(Resource):
    @api.doc('update an existing tag')
    def put(self, public_id):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")

        #retrieve the tag to be updated
        tag = TagService.get_a_tag(self, public_id)
        if not tag:
            api.abort(404, message="tag '{}' not found".format(public_id))

        #set new key/tags
        allowed_keys = tag.as_dict().keys()
        for key in data.keys():
            if key in allowed_keys:
                if key=='code':
                    existing_tag_with_new_code = TagService.get_a_tag(self, data[key])
                    if not existing_tag_with_new_code:
                        setattr(tag, key, data[key])
                    else:
                        #code tags must be unique for each tag
                        api.abort(409, message="tag code '{}' is duplicate".format(data[key]))
                else:
                    setattr(tag, key, data[key])
        try:
            TagService.commit()
            return tag.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e


@api.route('/delete_tag/<public_id>')
@api.param('public_id', 'The Tag identifier')
class Delete(Resource):
    @api.doc('delete a tag')
    def delete(self, public_id):
        tag = TagService.get_a_tag(self, public_id)
        if not tag:
            api.abort(404, message="tag '{}' not found".format(public_id))

        try:
            TagService.delete(tag)
            return tag.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
