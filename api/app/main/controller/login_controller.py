from datetime import datetime
from flask import current_app
import json
import jwt
import logging
import requests

from flask import Flask, request
from flask_restplus import Resource

from app.main import config
from app.main.model.login import Login
from app.main.util.dto import LoginDto
from app.main.service.login_service import save_new_user, get_a_user, user_commit

api = LoginDto.api


@api.route('/code_to_token', methods=['POST'])
class CodeToToken(Resource):
    def post(self):
        #call fence to exchange access code for tokens
        code = request.form['code']
        redirect_uri = request.form.get('redirect_uri')

        body = {
            "grant_type": "authorization_code",
            "client_id": config.Config.CLIENT_ID,
            "code": code,
            "redirect_uri": redirect_uri,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(
            "https://portal.pedscommons.org/user/oauth2/token",
            headers=headers,
            data=body
        )
        tokens = json.loads(response.text)

        #process tokens and store refresh_token
        refresh = tokens["refresh_token"]
        decoded_refresh = jwt.decode(refresh, verify=False)

        sub = decoded_refresh['sub'] #<- id
        iat = decoded_refresh['iat'] #<- issue date
        exp = decoded_refresh['exp'] #<- expiry date
        payload = {
            'id': int(sub),
            'refresh_token': refresh,
            'iat': datetime.fromtimestamp(iat).strftime('%Y-%m-%d %H:%M:%S'),
            'exp': datetime.fromtimestamp(exp).strftime('%Y-%m-%d %H:%M:%S')
        }
        with current_app.test_request_context("/login/create_user", method="POST", json=payload):
            try:
                response, status_code = Create().post()
            except Exception as e:
                logging.error(e, exc_info=True)
        
        if status_code==201:
            pass
        elif status_code==409:
            #id already there, do an update on the user doc
            with current_app.test_request_context("/login/update_user{}".format(payload['id']), method="PUT", json=payload):
                try:
                    response = Update().put(payload['id'])
                except Exception as e:
                    logging.error(e, exc_info=True)
                    api.abort(message='failed to create or update saved refresh_token') #if '404' in e:

        #finally, refresh token was stored, now return access_token to frontend
        try:
            return tokens['access_token']
        except Exception as e:
            logging.error(e, exc_info=True)

@api.route('/create_user')
class Create(Resource):
    @api.doc('add row to users')
    def post(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")

        template = Login()
        allowed_keys = template.as_dict().keys()

        new_user_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_user_dict.update({key:data[key]})

        try:
            response = save_new_user(new_user_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/update_user/<sub_id>')
@api.param('sub_id', "The User identifier. Primary key, 'id' in the table")
class Update(Resource):
    @api.doc('update an existing user')
    def put(self, sub_id):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")

        #retrieve the user to be updated
        user = get_a_user(sub_id)
        if not user:
            api.abort(404, message="user '{}' not found".format(sub_id))

        #set new key/values
        allowed_keys = user.as_dict().keys()
        for key in data.keys():
            if key in allowed_keys:
                if key=='code':
                    existing_user_with_new_code = get_a_user(data[key])
                    if not existing_user_with_new_code:
                        setattr(user, key, data[key])
                    else:
                        #code values must be unique for each user
                        api.abort(409, message="user code '{}' is duplicate".format(data[key]))
                else:
                    setattr(user, key, data[key])
        try:
            user_commit()
            return user.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
