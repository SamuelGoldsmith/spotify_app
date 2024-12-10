
import urllib.parse
from flask import render_template, flash, redirect, url_for

from app import db
from app.auth import auth_blueprint as bp_auth 
import sqlalchemy as sqla

import os
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.environ.get('CLIENT_ID') 
REDIRECT_URI = os.environ.get('REDIRECT_URI')
AUTH_URL = os.environ.get('AUTH_URL') 

@bp_auth.route('/login')
def login():
    scope = 'user-read-private user-read-email'

    params = {
        'client_id' : CLIENT_ID,
        'response_type' : 'code',
        'scope' : scope,
        'redirect_uri' : REDIRECT_URI,
        'show_dialog' : True
    }
    
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)
