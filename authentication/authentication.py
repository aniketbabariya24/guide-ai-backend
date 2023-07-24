from flask import Blueprint, request, jsonify
import os
from dotenv import load_dotenv
import jwt
from functools import wraps


load_dotenv()


def authentication(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = str(request.headers.get('Authorization'))
        if not token:
            return jsonify({"status": "error", "message": "Token is missing"}), 401
        try:
            data = jwt.decode(token, os.getenv(
                'JWT_SECRET'), algorithms=["HS256"])
            request.environ['influencer_id'] = data['influencer_id']
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 401
        return f(*args, **kwargs)
    return decorated


