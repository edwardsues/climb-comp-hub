from functools import wraps
from flask import request, jsonify
import asyncio
import os
from auth0_api_python.errors import BaseAuthError
from auth0_api_python import ApiClient, ApiClientOptions

from models import db, User

# initialize auth0 api client
api_client = ApiClient(ApiClientOptions(
    domain=os.getenv("AUTH0_DOMAIN"),
    audience=os.getenv("AUTH0_AUDIENCE")
))

def require_auth(f):
    """Auth0 decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid authorization header"}), 401
        
        token = auth_header.split(" ")[1]
        
        try:
            claims = asyncio.run(api_client.verify_access_token(token))
            g.user_claims = claims
            return f(*args, **kwargs)
        except BaseAuthError as e:
            return (
                jsonify({"error": str(e)}),
                e.get_status_code(),
                e.get_headers()
            )
    
    return decorated_function

def get_or_create_user():
    """Get user from Auth0 token, create if this is their first login. To be used whenever calling an endpoint that interacts with users."""
    auth0_id = request.current_user['sub']
    user = User.query.filter_by(auth0_id=auth0_id).first()

    # make a new user if one doesn't exist
    if not user:
        user = User(
            auth0_id=auth0_id,
            email=request.current_user.get('email'),
            name=request.current_user.get('name'),
            role='climber'
        )
        db.session.add(user)
        db.session.commit()
    return user

    