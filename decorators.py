from flask import request, make_response
from flask import session, redirect, url_for,request
import configparser
from google.auth.transport import requests
from google.oauth2 import id_token
from ib_aitool import app
from functools import wraps
from ib_aitool.database.models.User import User
from sqlalchemy import and_

config = configparser.ConfigParser()
config.read('demo-config.ini')

def xr_login_required(func):
    def wrapper(*args, **kwargs):
        if 'auth-cookie' in request.cookies and request.cookies['auth-cookie']:
            token = request.cookies.get('auth-cookie').replace(" ","")
        else:
            token = request.args.get('token')
            if token is None:
                return redirect(config.get('REACT', 'REACT_APP'))
            token = token.replace(" ","")
            resp = make_response(func(*args, **kwargs))
            resp.set_cookie('auth-cookie', token)
            return resp

        result = verify_google_token(token, config.get('Google', 'GOOGLE_CLIENT_ID_JWT'))

        if result:
            return func(*args, **kwargs)
        else:
            print("Invalid Token")
            return redirect(config.get('REACT', 'REACT_APP'))
    return wrapper



def verify_google_token(id_token_str, client_id):
    try:
        id_info = id_token.verify_oauth2_token(id_token_str, requests.Request(), client_id)
        email = id_info['email']

        email_condition = User.email == email
        is_logged_in_condition = User.is_logged_in == True

        conditions = and_(email_condition, is_logged_in_condition)
        user = User.query.filter(conditions).all()

        if user:
            return True
        else:
            return None
    except ValueError as e:
        print(f"Error verifying Google token: {e}")
        return None

def current_user():
    if 'auth-cookie' in request.cookies:
        token = request.cookies.get('auth-cookie').replace(" ","")
    else:
       return redirect(config.get('REACT', 'REACT_APP'))

    token = request.cookies.get('auth-cookie').replace(" ","")
    id_info = id_token.verify_oauth2_token(token, requests.Request(), config.get('Google', 'GOOGLE_CLIENT_ID_JWT'))
    email = id_info['email']
    email_condition = User.email == email
    is_logged_in_condition = User.is_logged_in == 1

    conditions = and_(email_condition, is_logged_in_condition)
    user = User.query.filter(conditions).all()

    if user:
        current_user = {"id":user[0].id,"role":user[0].role_id,"email": user[0].email}
        return current_user
    else:
        return None