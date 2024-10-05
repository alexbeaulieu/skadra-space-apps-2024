from flask import Flask
from routes import register_routes
from pipelineManager import pipeline_manager


app = Flask(__name__)

# Start the Flask development server
if __name__ == "__main__":
    # register filters
    pipeline_manager = pipeline_manager()
    register_routes(app)
    
    app.run(debug=True)