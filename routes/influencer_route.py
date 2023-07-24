from flask import Blueprint, request, jsonify
from schemamodels.influencers import InfluencersModel
from dotenv import load_dotenv
from bson import ObjectId
from config.db import influencers_collection
import os
import bcrypt
import jwt
from authentication.authentication import authentication

load_dotenv()

influencer_bp = Blueprint('influencer_bp', __name__)


@influencer_bp.route('/register', methods=['POST'])
def register_influencer():
    try:
        body = request.json
        isPresent = influencers_collection.find_one({"email": body['email']})
        if isPresent:
            return jsonify({"status": "error", "message": "Account Already Exists"}), 400
        influencer = InfluencersModel(**body)
        influencers_collection.insert_one(influencer.__dict__)
        return jsonify({"status": "success", "message": "Registeration Successful"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@influencer_bp.route('/login', methods=['POST'])
def login_influencer():
    try:
        body = request.json
        influencer = influencers_collection.find_one({"email": body['email']})
        if influencer:
            validPass = bcrypt.checkpw(
                body['password'].encode('utf-8'), influencer['password'])

            if validPass:
                token = jwt.encode({"influencer_id": str(influencer['_id'])}, "masai", algorithm="HS256")
                return jsonify({"status": "success", "message": "Login Successful", "token": token}), 200
            else:
                return jsonify({"status": "error", "message": "Invalid Credentials"}), 400
        else:
            return jsonify({"status": "error", "message": "Account Does Not Exists"}), 400
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)}), 400


@influencer_bp.route('/get-influencer', methods=['GET'])
@authentication
def get_influencer():
    influencer_id = request.environ['influencer_id']
    try:
        influencer = influencers_collection.find_one(
            {"_id": ObjectId(influencer_id)})

        data = influencer.copy()
        data.pop('password')
        data['_id'] = str(data['_id'])
        return jsonify({"status": "success", "data": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
