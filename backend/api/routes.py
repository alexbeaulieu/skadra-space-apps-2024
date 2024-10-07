import glob
import re
from flask import Blueprint, request, jsonify, g
import os
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import io
import base64

from filters.filterDto import FilterDto

matplotlib.use('Agg')

dtFmt = mdates.DateFormatter('%H:%M') # define the plot date formatting


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
        

        fig,ax = plt.subplots(2,1,figsize=(12,6), sharex=True, sharey=True)

        # Generate the plot and send it back to the client
        # Show raw data
        data.plot(y="velocity", ax=ax[0], title="Raw data", label='_Hidden')
        ax[0].tick_params(axis='x',labelbottom='off')
        ax[0].tick_params(axis='both' , direction='in', top=True, right=True)
        ax[0].xaxis.set_major_formatter(dtFmt)


        # Show filtered data
        cleaned_data.plot(y="velocity", ax=ax[1], title="Clean data", legend=False)
        ax[1].tick_params(axis='both' , direction='in', top=True, right=True) 


        # Add detections
        qtimes = data["mq_type_id"].dropna().index
        qtypes = data["mq_type_id"].dropna().values
        for i, (qtime, qtype) in enumerate(zip(qtimes, qtypes)):
            ax[0].axvline(x=qtime, c="red", label= "True quake" if i==0  else "_Hidden")
            ax[1].axvline(x=qtime, c="red", label= "True quake" if i==0  else "_Hidden")


        tr_times = data.index.values
        for i,e in enumerate(extrapolated_data):
            ax[0].axvline(x=tr_times[e][0], c="gray", ls=":", marker='d', markerfacecolor='black', markeredgecolor='black', label= "Detected quake" if i==0  else "_Hidden")
            ax[1].axvline(x=tr_times[e][0], c="gray", ls=":", marker='d', markerfacecolor='black', markeredgecolor='black', label= "Detected quake" if i==0  else "_Hidden")



        ax[0].legend(loc='lower left')
        ax[1].set_xlabel("Time of the day")
        
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
    
    
    