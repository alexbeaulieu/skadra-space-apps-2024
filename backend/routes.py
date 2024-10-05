from flask import Blueprint, request, jsonify

from pipelineManager import pipeline_manager

api = Blueprint('api', __name__)

def register_routes(app):
    app.register_blueprint(api)

@api.route('/')
def home():
    return "Hello, Flask!"

@api.route('/about')
def about():
    return "About page"

@api.route('/planets', methods=['GET'])
def get_all_planets():
    raise NotImplementedError()

@api.route('/planets/<int:planet_id>/dates', methods=['GET'])
def get_planet(planet_id):
    raise NotImplementedError()

@api.route('/planets/<int:planet_id>/<int:date>', methods=['GET'])
def get_planet_specs(planet_id, date):
    raise NotImplementedError()

@api.route('/planets/<int:planet_id>/<int:date>', methods=['POST'])
def process_data(planet_id, date):
    data = request.json
    class FilterDto:
        def __init__(self, filter_type, value):
            self.filter_type = filter_type
            self.value = value

    filterDtos = [FilterDto(**item) for item in data]
    return pipeline_manager().process(filterDtos, planet_id, date)

