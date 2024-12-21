from datetime import datetime
from functools import wraps
import sys
from flask import render_template, flash, redirect, url_for, request, jsonify, session
import sqlalchemy as sqla
import requests
from app import db

from app.main import main_blueprint as bp_main
import os
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.environ.get('CLIENT_ID') 
CLIENT_SECRET = os.environ.get('CLIENT_SECRET') 
REDIRECT_URI = os.environ.get('REDIRECT_URI')
AUTH_URL = os.environ.get('AUTH_URL') 
TOKEN_URL = os.environ.get('TOKEN_URL') 
API_BASE_URL = os.environ.get('API_BASE_URL') 

def token(func):
    @wraps(func)
    def p(*args, **kwargs):
        if 'access_token' not in session:
            return redirect(url_for('auth.login'))
        if datetime.now().timestamp() >= session['expires_at']:
            return redirect(url_for('main.refresh_token'))
        return func(*args, **kwargs)
    return p

@bp_main.route('/', methods=['GET'])
@bp_main.route('/index', methods=['GET'])
def index():

    return render_template('index.html', title="home")


@bp_main.route('/callback', methods=['GET'])
def callback():
    if 'error' in request.args:
        return jsonify({"error" : request.args['error']})
    if 'code' in request.args:
        req_body = {
            'code' : request.args['code'],
            'grant_type' : 'authorization_code',
            'redirect_uri' : REDIRECT_URI,
            'client_id' : CLIENT_ID,
            'client_secret' : CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data = req_body)
        token_info = response.json()
        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

    return redirect(url_for('main.playlists'))

@token
@bp_main.route('/playlists', methods=['GET'])
def playlists():
    # if 'access_token' not in session:
    #     return redirect(url_for('auth.login')) TODO Uncomment if error
    # if datetime.now().timestamp() >= session['expires_at']:
    #     return redirect(url_for('main.refresh_token'))
    
    headers = {
        'Authorization' : f"Bearer {session['access_token']}"
    }

    response = requests.get(API_BASE_URL + 'me/playlists', headers=headers)
    playlists = response.json()

    # return jsonify(playlists)
    return render_template('playlists.html', playlists = playlists['items'])
@token
@bp_main.route('/artists/top', methods=['GET'])
def top_artists():
    # if 'access_token' not in session:
    #     return redirect(url_for('auth.login')) TODO Uncomment if error
    # if datetime.now().timestamp() >= session['expires_at']:
    #     return redirect(url_for('main.refresh_token'))
    
    headers = {
        'Authorization' : f"Bearer {session['access_token']}"
    }
    print("hi")
    response = requests.get(API_BASE_URL + 'me/top/artists', headers=headers)
    artists = response.json()
    print(artists)
    return jsonify(artists)
    return render_template('index.html')

@bp_main.route('/refresh-token', methods=['GET'])
def refresh_token():
    if 'refresh_token' not in session:
        return redirect(url_for('auth.login'))
    if datetime.now().timestamp() >= session['expires_at']:
        req_body = {
            'grant_type' : 'refresh_token',
            'refresh_token' : session['refresh_token'],
            'client_id' : CLIENT_ID,
            'client_secret' : CLIENT_SECRET
        }
        response = requests.post(TOKEN_URL, data=req_body)
        new_token_info = response.json()
        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']

        return redirect(url_for('main.index'))