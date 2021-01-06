from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.model.xyz import Xyz
from app.main.service.xyz_service import XyzService
from app.main.util import AlchemyEncoder
from app.main.util.dto import XyzDto


api = XyzDto.api
_xyz = XyzDto.xyz


@api.route('/<public_id>')
@api.param('public_id', 'The Xyz identifier')
class XyzInfo(Resource):
    @api.doc('get a xyz')
    @api.marshal_with(_xyz)
    def get(self, public_id):
        #DEBUG
        #xyz = XyzService.get_a_xyz(public_id)
        xyz = XyzService.get_a_xyz(self, public_id)
        if not xyz:
            api.abort(404, message="xyz '{}' not found".format(public_id))
        else:
            return xyz.as_dict()


@api.route('/info')
class AllXyzsInfo(Resource):
    def get(self):
        xyzs = XyzService.get_all(Xyz)
        try:
            if xyzs:
                body = [r.as_dict() for r in xyzs]
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
            api.abort(404, message="xyz table not found or has no data")


@api.route('/create_xyz')
class Create(Resource):
    @api.doc('create a new xyz')
    def post(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        template = Xyz()
        allowed_keys = template.as_dict().keys()

        new_xyz_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_xyz_dict.update({key:data[key]})
        try:

            #DEBUG
            #response = XyzService.save_new_xyz(new_xyz_dict)
            #response = XyzService.save_new_xyz(self, new_xyz_dict)
            #response = XyzService.save_new_xyz(Xyz, new_xyz_dict)
            response = XyzService.save_new_xyz(XyzService, new_xyz_dict)

            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/update_xyz/<public_id>')
@api.param('public_id', 'The Xyz identifier')
class Update(Resource):
    @api.doc('update an existing xyz')
    def put(self, public_id):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")

        #retrieve the xyz to be updated

        #DEBUG
        #xyz = XyzService.get_a_xyz(public_id)
        xyz = XyzService.get_a_xyz(self, public_id)

        if not xyz:
            api.abort(404, message="xyz '{}' not found".format(public_id))

        #set new key/values
        allowed_keys = xyz.as_dict().keys()
        for key in data.keys():
            if key in allowed_keys:
                if key=='code':

                    #DEBUG
                    #existing_xyz_with_new_code = XyzService.get_a_xyz(data[key])
                    existing_xyz_with_new_code = XyzService.get_a_xyz(self, data[key])
                    
                    if not existing_xyz_with_new_code:
                        setattr(xyz, key, data[key])
                    else:
                        #code values must be unique for each xyz
                        api.abort(409, message="xyz code '{}' is duplicate".format(data[key]))
                else:
                    setattr(xyz, key, data[key])
        try:
            XyzService.commit()
            return xyz.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e


@api.route('/delete_xyz/<public_id>')
@api.param('public_id', 'The Xyz identifier')
class Delete(Resource):
    @api.doc('delete a xyz')
    def delete(self, public_id):

        #DEBUG
        #xyz = XyzService.get_a_xyz(public_id)
        xyz = XyzService.get_a_xyz(self, public_id)
        
        if not xyz:
            api.abort(404, message="xyz '{}' not found".format(public_id))

        try:
            XyzService.delete(xyz)
            return xyz.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
