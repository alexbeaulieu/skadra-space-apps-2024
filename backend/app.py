from flask import Flask
from routes import register_routes
from pipelineManager import PipelineManager
from flask import g

app = Flask(__name__)

@app.before_request
def before_request():
    g.pipeline_manager = pipeline_manager

register_routes(app)

# Start the Flask development server
if __name__ == "__main__":
    # register filters
    pipeline_manager = PipelineManager()
    
    app.run(debug=True)