from flask import Flask
from api.routes import register_routes
from algorithms.algorithmManager import AlgorithmManager
from algorithms.short_long_term_average_algo import ShortLongTermAverageAlgorithm
from filters.bandpass_filter import BandpassFilter
from filters.remove_peaks_filter import RemovePeaksFilter
from filters.lowpass_filter import LowpassFilter
from filters.pipelineManager import PipelineManager
from flask import g
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.before_request
def before_request():
    g.pipeline_manager = pipeline_manager
    g.algo_manager = algo_manager

register_routes(app)

# register filters
pipeline_manager = PipelineManager()
bandpass_filter = BandpassFilter()
remove_peaks_filter = RemovePeaksFilter()
low_pass_filter = LowpassFilter()

pipeline_manager.add_filter(remove_peaks_filter)
pipeline_manager.add_filter(bandpass_filter)
pipeline_manager.add_filter(low_pass_filter)


# register algorithms
algo_manager = AlgorithmManager()
short_long_term_average_algo = ShortLongTermAverageAlgorithm()
algo_manager.add_algorithm(short_long_term_average_algo)