import glob
import re
from flask import Blueprint, request, jsonify, g
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64


from filters.filterDto import FilterDto

# Create a Blueprint for the routes
api = Blueprint('api', __name__)
def register_routes(app):
    app.register_blueprint(api)


@api.route('/')
def home():
    return "Hello, Flask!"

@api.route('/about')
def about():
    return "About page"

@api.route('/planets/', methods=['GET'])
def get_all_planets():
    data_directory = os.path.join(os.path.dirname(__file__), '..', 'data')
    try:
        folders = [name for name in os.listdir(data_directory) if os.path.isdir(os.path.join(data_directory, name))]
        return jsonify(folders)
    except FileNotFoundError:
        return jsonify({"error": "Data folder not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/planets/<planet_name>/dates/', methods=['GET'])
def get_planet_dates(planet_name):
    try:
        data_directory = os.path.join(os.path.dirname(__file__), '..', 'data', planet_name)
        files  =  glob.glob(data_directory+"/**/*.parquet", recursive=True)
        dates = [re.search("\d{4}-\d{2}-\d{2}", file)[0] for file in files]
        return jsonify(dates)
    except FileNotFoundError:
        return jsonify({"error": "Data folder not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/filters/', methods=['GET'])
def get_all_filters():
    filters = g.pipeline_manager.get_filters()
    return jsonify([{"name": f.name, "params": f.params} for f in filters])

@api.route('/algos/', methods=['GET'])
def get_all_algos():
    algos = g.algo_manager.get_algorithms()
    return jsonify([{"name": a.name} for a in algos])

@api.route('/planets/<planet_name>/<date>/<algo_name>/', methods=['POST']) # triggered when a date gets selected
def process_data(planet_name, date, algo_name):
    try:
        # Get the filter specs from the request
        req = request.json
        filterDtos = [FilterDto(**item) for item in req]

        # Load the data
        data_directory = os.path.join(os.path.dirname(__file__), '..', 'data', planet_name)
        files  =  glob.glob(data_directory+"/**/*.parquet", recursive=True)
        file = next((f for f in files if date in f), None)
        if file is None:
            return jsonify({"error": "File for the specified date not found"}), 404
        data = pd.read_parquet(file)
        
        cleaned_data = g.pipeline_manager.process(order = filterDtos, data =data)
        
        tr = cleaned_data.copy()
        print(f"options : {tr.index}")
        tr_times = tr.index.to_numpy()
        tr_data = tr['velocity'].to_numpy()
        print("tr_times : " , tr_times)
        print("tr_data : " , tr_data)
        
        extrapolated_data = g.algo_manager.process(algo_name, cleaned_data)
        
        # generate the plot and send it back to the client
        fig,ax = plt.subplots(1,1,figsize=(12,3))
        for i in np.arange(0,len(extrapolated_data)):
            triggers = extrapolated_data[i]
            ax.axvline(x = tr_times[triggers[0]], color='red', label='Trig. On')
            ax.axvline(x = tr_times[triggers[1]], color='purple', label='Trig. Off')
        
        # Plot seismogram
        ax.plot(tr_times,tr_data)
        ax.set_xlim([min(tr_times),max(tr_times)])
        ax.legend()
        # Save the plot to a buffer
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        
        # Encode the buffer in base64
        plot_png_base64 = base64.b64encode(buf.read()).decode('utf-8')
        
        # Optionally close the figure to free memory
        plt.close(fig)

        return jsonify({'plot_html': plot_png_base64})
    except FileNotFoundError:
        return jsonify({"error": "Data folder not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
    