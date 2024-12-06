from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
import importlib
import threading
import time
from waitress import serve
from pathlib import Path

class ModelServer:
    def __init__(self, models_path: str | Path = './models', port: int = 4299):
        """Initialize the Model Server

        Args:
            models_path (str | Path): Path to the directory containing model files
            port (int): Port number to run the server on
        """
        self.models_path = Path(models_path)
        self.port = port
        self.app = Flask(__name__)
        CORS(self.app)
        self.models = {}
        self.model_lock = threading.Lock()
        
        # Setup routes
        self.setup_routes()
        
        # Start cleanup thread
        self.cleanup_thread = threading.Thread(target=self._model_cleanup, daemon=True)
        self.cleanup_thread.start()

    def setup_routes(self):
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Simple endpoint to verify client server is running"""
            return jsonify({
                "status": "ok", 
                "message": "Client server is running",
                "models_path": str(self.models_path),
                "port": self.port
            }), 200

            
        @self.app.route('/testlocalchat', methods=['POST'])
        def testlocalchat():
            data = request.get_json()
            
            if data and 'message' in data and 'model' in data:
                user_message = data['message']
                model_name = data['model'][:-3]
                print(model_name)
                test_model = importlib.import_module(f'models.{model_name}')
                response = test_model.chat(user_message)
                
                if response:
                    return jsonify(message=response, trigger=True), 200
                else:
                    return jsonify(message="No message provided", trigger=False), 400
            else:
                return jsonify(message="Invalid request data", trigger=False), 400

        @self.app.route('/get_existing_models', methods=['GET'])
        def get_existing_models():
            model_files = []
            for f in os.listdir(self.models_path):
                full_path = os.path.join(self.models_path, f)
                if os.path.isfile(full_path):
                    creation_time = os.path.getctime(full_path)
                    formatted_time = datetime.fromtimestamp(creation_time).strftime('%Y/%m/%d %H:%M:%S')
                    model_files.append((f, formatted_time))
            return jsonify(message=model_files, trigger=True), 200

        @self.app.route('/chat', methods=['POST'])
        def chat():
            data = request.get_json()
            prompt = data.get('prompt')
            process_id = data.get('process_id')
            model_name = data.get('model_name')
            finish_flag = data.get('finish_flag')
            
            model = self._get_model(process_id, model_name)
            
            try:
                answer = model(prompt)
                
                if finish_flag:
                    with self.model_lock:
                        if process_id in self.models:
                            del self.models[process_id]
                
                return jsonify({'answer': answer})
            except Exception as e:
                return jsonify({'error': str(e)}), 500

    def _load_model(self, model_name):
        model_module = importlib.import_module(f'models.{model_name[:-3]}')
        importlib.reload(model_module)
        return model_module.chat

    def _get_model(self, process_id, model_name):
        with self.model_lock:
            if process_id not in self.models:
                self.models[process_id] = {
                    'model': self._load_model(model_name),
                    'last_accessed': time.time()
                }
            self.models[process_id]['last_accessed'] = time.time()
            return self.models[process_id]['model']

    def _model_cleanup(self):
        while True:
            time.sleep(60)
            with self.model_lock:
                current_time = time.time()
                for process_id in list(self.models.keys()):
                    if current_time - self.models[process_id]['last_accessed'] > 180:
                        del self.models[process_id]

    def start(self):
        """Start the server"""
        print(f"Starting Model Server on http://127.0.0.1:{self.port}")
        print(f"Models path: {self.models_path}")
        serve(self.app, host='0.0.0.0', port=self.port)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Run the model server")
    parser.add_argument('--port', type=int, default=4299, 
                       help='Port number to run the server on (default: 4299)')
    parser.add_argument('--models-path', type=str, default='./models',
                       help='Path to models directory (default: ./models)')
    args = parser.parse_args()
    
    server = ModelServer(models_path=args.models_path, port=args.port)
    server.start()