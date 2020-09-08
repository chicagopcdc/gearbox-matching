from datetime import datetime, date
from flask import current_app, jsonify
import json
import jwt
import logging
from time import gmtime, strftime
import requests

from flask import Flask, request
from flask_restplus import Resource

from app.main import config
from app.main.model.login import Login
from app.main.service.login_service import LoginService
from app.main.util.dto import LoginDto

api = LoginDto.api
_login = LoginDto.login

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
        try:
            refresh = tokens["refresh_token"]
            decoded_refresh = jwt.decode(refresh, verify=False)
        except Exception as e:
            logging.error(e, exc_info=True)
            message_text = """tokens not received: is CLIENT_ID set/passed to container? Secrets/creds.json should have format like: {"CLIENT_ID": "__client_id__"}"""
            api.abort(message=message_text)
            
        sub_id = decoded_refresh['sub'] #<- user id from fence
        iat = decoded_refresh['iat'] #<- issue date
        exp = decoded_refresh['exp'] #<- expiry date
        payload = {
            'sub_id': sub_id,
            'refresh_token': refresh,
            'iat': datetime.fromtimestamp(iat).strftime('%Y-%m-%d %H:%M:%S'),
            'exp': datetime.fromtimestamp(exp).strftime('%Y-%m-%d %H:%M:%S')
        }
        with current_app.test_request_context("/login/create_login", method="POST", json=payload):
            try:
                response, status_code = Create().post()
            except Exception as e:
                logging.error(e, exc_info=True)
        
        if status_code==201:
            pass
        elif status_code==409:
            #sub_id already there, do an update on the login doc
            with current_app.test_request_context("/login/update_login{}".format(payload['sub_id']), method="PUT", json=payload):
                try:
                    response = Update().put(payload['sub_id'])
                except Exception as e:
                    logging.error(e, exc_info=True)
                    api.abort(message='failed to create or update saved refresh_token') #if '404' in e:

        #finally, refresh token was stored, now return access_token to frontend
        try:
            return tokens['access_token']
        except Exception as e:
            logging.error(e, exc_info=True)

@api.route('/create_login')
class Create(Resource):
    @api.doc('add row to login table')
    def post(self):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")

        template = Login()
        allowed_keys = template.as_dict().keys()

        new_login_dict = {}
        for key in data.keys():
            if key in allowed_keys:
                new_login_dict.update({key:data[key]})

        try:
            response = LoginService.save_new_login(new_login_dict)
            return response
        except Exception as e:
            logging.error(e, exc_info=True)


@api.route('/<sub_id>')
@api.param('sub_id', 'The User Login identifier')
class LoginInfo(Resource):
    @api.doc('get login info')
    @api.marshal_with(_login)
    def get(self, sub_id):
        login = LoginService.get_a_login(sub_id)
        if not login:
            api.abort(404, message="user login '{}' not found".format(sub_id))
        else:
            return login.as_dict()


@api.route('/info')
class AllLoginsInfo(Resource):
    def get(self):
        logins = LoginService.get_all(Login)
        try:
            if logins:
                body = [r.as_dict() for r in logins]
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
            api.abort(404, message="login table not found or has no data")


@api.route('/update_login/<sub_id>')
@api.param('sub_id', "The Login/User identifier. Primary key, 'id' in the table")
class Update(Resource):
    @api.doc('update an existing login')
    def put(self, sub_id):
        data = api.payload
        if not data or not isinstance(data, dict):
            api.abort(400, message="null payload or payload not json/dict")

        #retrieve the login to be updated
        login = LoginService.get_a_login(sub_id)
        if not login:
            api.abort(404, message="login info '{}' not found".format(sub_id))

        #set new key/values
        allowed_keys = login.as_dict().keys()
        for key in data.keys():
            if key in allowed_keys:
                if key=='code':
                    existing_login_with_new_code = LoginService.get_a_login(data[key])
                    if not existing_login_with_new_code:
                        setattr(login, key, data[key])
                    else:
                        #code values must be unique for each login
                        api.abort(409, message="user login code '{}' is duplicate".format(data[key]))
                else:
                    setattr(login, key, data[key])
        try:
            LoginService.commit()
            return login.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e


@api.route('/delete_login/<sub_id>')
@api.param('sub_id', 'The User Login identifier')
class Delete(Resource):
    @api.doc('delete a login')
    def delete(self, sub_id):
        login = LoginService.get_a_login(sub_id)
        if not login:
            api.abort(404, message="user login '{}' not found".format(sub_id))

        try:
            LoginService.delete(login)
            return login.as_dict()
        except Exception as e:
            logging.error(e, exc_info=True)
            return e
