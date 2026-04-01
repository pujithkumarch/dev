from flask import Flask, jsonify
import os

def create_app():
    app = Flask(__name__)

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({
            'status': 'ok',
            'env': os.getenv('APP_ENV', 'dev')
        })

    @app.route('/api/v1/data', methods=['GET'])
    def get_data():
        return jsonify({
            'message': 'Hello from Flask REST API'
        })

    return app
