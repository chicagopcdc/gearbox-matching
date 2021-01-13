from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.model.site import Site
from app.main.service.site_service import SiteService
from app.main.util import AlchemyEncoder
from app.main.util.dto import SiteDto


api = SiteDto.api
_site = SiteDto.site


@api.route('/<public_id>')
@api.param('public_id', 'The Site identifier')
class SiteInfo(Resource):
    @api.doc('get a site')
    @api.marshal_with(_site)
    def get(self, public_id):
        site = SiteService.get_a_site(self, public_id)
        if not site:
            api.abort(404, message="site '{}' not found".format(public_id))
        else:
            return site.as_dict()


@api.route('/info')
class AllSitesInfo(Resource):
    def get(self):
        sites = SiteService.get_all(Site)
        try:
            if sites:
                body = [r.as_dict() for r in sites]
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
            api.abort(404, message="site table not found or has no data")


@api.route('/create_site')
class Create(Resource):
    @api.doc('create a new site')
    def post(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        template = Site()
        allowed_keys = template.as_dict().keys()

        new_site_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_site_dict.update({key:data[key]})
        try:
            response = SiteService.save_new_site(SiteService, new_site_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/update_site/<public_id>')
@api.param('public_id', 'The Site identifier')
class Update(Resource):
    @api.doc('update an existing site')
    def put(self, public_id):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")

        #retrieve the site to be updated
        site = SiteService.get_a_site(self, public_id)
        if not site:
            api.abort(404, message="site '{}' not found".format(public_id))

        #set new key/values
        allowed_keys = site.as_dict().keys()
        for key in data.keys():
            if key in allowed_keys:
                if key=='code':
                    existing_site_with_new_code = SiteService.get_a_site(self, data[key])
                    if not existing_site_with_new_code:
                        setattr(site, key, data[key])
                    else:
                        #code values must be unique for each site
                        api.abort(409, message="site code '{}' is duplicate".format(data[key]))
                else:
                    setattr(site, key, data[key])
        try:
            SiteService.commit()
            return site.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e


@api.route('/delete_site/<public_id>')
@api.param('public_id', 'The Site identifier')
class Delete(Resource):
    @api.doc('delete a site')
    def delete(self, public_id):
        site = SiteService.get_a_site(self, public_id)
        if not site:
            api.abort(404, message="site '{}' not found".format(public_id))

        try:
            SiteService.delete(site)
            return site.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
