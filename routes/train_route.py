from flask import Blueprint, request, jsonify
from bson import ObjectId
import json
import chardet
from train.json_convert import converToJsonviaChat
# models
from schemamodels.transcripts import TranscriptsModel
from schemamodels.qna import QnAModel

# collections
from config.db import transcripts_collection
from config.db import qna_collection
from config.db import influencers_collection


# authentication
from authentication.authentication import authentication

# trainer prompt
from train.trainer_prompt import chatGenResp

train_bp = Blueprint('train_bp', __name__)


@train_bp.route('/add-transcript', methods=['POST'])
@authentication
def add_transcript():
    try:
        body = request.json
        influencer_id = request.environ['influencer_id']
        # check if trasncipt of the influencer already exists
        transcript = transcripts_collection.find_one(
            {"influencer_id": ObjectId(influencer_id), "transcript": body['transcript']})
        if transcript:
            return jsonify({"status": "error", "message": "Transcript already exists"}), 400
        transcript = TranscriptsModel(
            influencer_id=influencer_id, transcript=body['transcript'])
        transcripts_collection.insert_one(transcript.__dict__)
        return jsonify({"status": "success", "message": "Transcript Added"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@train_bp.route('/add-transcript-file', methods=['POST'])
@authentication
def add_transcript_file():
    try:
        influencer_id = request.environ['influencer_id']
        # get the file from the request body
        file = request.files['file']
        json_result = converToJsonviaChat(file, "trasncript", influencer_id)

        json_result = json.loads(json_result)
        if json_result["ok"]:
            return jsonify({"status": "success", "message": "Transcript Added"}), 201
        else:
            return jsonify({"status": "error", "message": str(json_result["message"])}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": "Error in adding the file, check type"}), 400


@train_bp.route('/get-transcripts', methods=['GET'])
@authentication
def get_transcripts():
    influencer_id = request.environ['influencer_id']
    try:
        transcripts = list(transcripts_collection.find(
            {"influencer_id": ObjectId(influencer_id)}))
        return jsonify({"status": "success", "data": transcripts}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@train_bp.route('/add-qnas', methods=['POST'])
@authentication
def add_qna():
    body = request.json
    influencer_id = request.environ['influencer_id']
    try:
        qna = QnAModel(influencer_id=influencer_id,
                       sample_question=body['sample_question'], sample_answer=body['sample_answer'])
        qna_collection.insert_one(qna.__dict__)
        return jsonify({"status": "success", "message": "QnA Added"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@train_bp.route('/add-qnas-file', methods=['POST'])
@authentication
def add_qnas_file():
    try:
        influencer_id = request.environ['influencer_id']
        # get the file from the request body
        file = request.files['file']
        # json conversion
        json_result = converToJsonviaChat(file, "qna", influencer_id)

        json_result = json.loads(json_result)
        if json_result["ok"]:
            return jsonify({"status": "success", "message": "QnAs Added"}), 201
        else:
            return jsonify({"status": "error", "message": 'File is not compatible'}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": "Error in adding the file, check type"}), 400


@train_bp.route('/get-qnas', methods=['GET'])
@authentication
def get_qna():
    influencer_id = request.environ['influencer_id']
    try:
        qnas = list(qna_collection.find(
            {"influencer_id": ObjectId(influencer_id)}))

        for qna in qnas.copy():
            qna['_id'] = str(qna['_id'])
            qna['influencer_id'] = str(qna['influencer_id'])
        return jsonify({"status": "success", "data": qnas}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@train_bp.route("/train", methods=['GET'])
@authentication
def train():
    influencer_id = request.environ['influencer_id']
    try:
        transcripts = list(transcripts_collection.find(
            {"influencer_id": ObjectId(influencer_id)}))
        sampleQnA = list(qna_collection.find(
            {"influencer_id": ObjectId(influencer_id)}))
        prompt = trainer_prompt(sampleQnA, transcripts)
        print(prompt)
        return jsonify({"status": "success", "message": "Training Complete"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@train_bp.route("/generate-response", methods=['POST'])
@authentication
def generate_response():
    body = request.json
    try:
        influencer_id = ObjectId(request.environ['influencer_id'])
        influencer = influencers_collection.find_one(
            {"_id": influencer_id})
        if not influencer:
            return jsonify({"status": "error", "message": "Error generating response"}), 404
        response = chatGenResp(body['query'])

        return jsonify({"status": "success", "data": response}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
