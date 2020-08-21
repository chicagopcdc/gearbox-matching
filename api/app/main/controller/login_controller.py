import json
import logging
import requests

from flask import Flask, request
from flask_restplus import Resource

from app.main.util.dto import LoginDto

api = LoginDto.api


@api.route('/code_to_token', methods=['POST'])
class CodeToToken(Resource):
    def post(self):
        code = request.form['code']
        redirect_uri = request.form.get('redirect_uri')

        body = {
            "grant_type": "authorization_code",
            "client_id": "VAyVF4wMjyD7FBAVKIiZevlt80A4LNIT7O9SZ6vu",
            "code": code,
            "redirect_uri": redirect_uri,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(
            "https://portal.pedscommons.org/user/oauth2/token",
            headers=headers,
            data=body
        )

        try:
            return json.loads(response.text)['access_token']
        except Exception as e:
            logging.error(e, exc_info=True)

