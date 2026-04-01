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
```

---

### File 5: `requirements.txt`

Check if it exists — if not, add it:
```
flask==3.0.0
gunicorn==21.2.0
pytest==7.4.0
