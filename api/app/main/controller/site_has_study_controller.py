from flask import request, jsonify
from flask_restplus import Resource
from datetime import date
import logging
from time import gmtime, strftime
import json

from app.main.model.site_has_study import SiteHasStudy
from app.main.service.site_has_study_service import SiteHasStudyService
from app.main.util import AlchemyEncoder
from app.main.util.dto import SiteHasStudyDto


api = SiteHasStudyDto.api
_site_has_study = SiteHasStudyDto.site_has_study


@api.route('')
class SiteHasStudyInfo(Resource):
    @api.doc('get a site_has_study')
    @api.marshal_with(_site_has_study)
    def get(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        site_has_study = SiteHasStudyService.get_a_site_has_study(self, data)
        if not site_has_study:
            api.abort(404, message="site_has_study '{}' not found".format(data))
        else:
            return site_has_study.as_dict()


@api.route('/info')
class AllSiteHasStudiesInfo(Resource):
    def get(self):
        site_has_studies = SiteHasStudyService.get_all(SiteHasStudy)
        try:
            if site_has_studies:
                body = [r.as_dict() for r in site_has_studies]
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
            api.abort(404, message="site_has_study table not found or has no data")


@api.route('/create_site_has_study')
class Create(Resource):
    @api.doc('create a new site_has_study')
    def post(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        template = SiteHasStudy()
        allowed_keys = template.as_dict().keys()

        new_site_has_study_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_site_has_study_dict.update({key:data[key]})
        try:
            response = SiteHasStudyService.save_new_site_has_study(SiteHasStudyService, new_site_has_study_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/delete_site_has_study')
class Delete(Resource):
    @api.doc('delete a site_has_study')
    def delete(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")
        site_has_study = SiteHasStudyService.get_a_site_has_study(self, data)
        if not site_has_study:
            api.abort(404, message="site_has_study '{}' not found".format(data))

        try:
            SiteHasStudyService.delete(site_has_study)
            return site_has_study.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
