from pipelineManager import PipelineManager
from flask import Flask


app = Flask(__name__)

# Define a basic route
@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/about')
def about():
    return "About page"
# Start the Flask development server
if __name__ == "__main__":
    # register filters
    cleaners = PipelineManager()
    
    
    app.run(debug=True)