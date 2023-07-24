from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
# routes
from routes.influencer_route import influencer_bp
from routes.train_route import train_bp

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def api():
    return jsonify({'message': 'Hello, World!'})


app.register_blueprint(influencer_bp, url_prefix='/api/v1/influencers')
app.register_blueprint(train_bp, url_prefix='/api/v1/train')


if __name__ == '__main__':
    app.run()
