from flask import Flask, request, jsonify
from ctgan import CTGAN, load_demo
import pickle
import pandas as pd
import json
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


def fit_model(data, discrete_columns, model_path='syntheticDataModel.pkl'):
    # Initialize the CTGAN model with desired settings
    ctgan_model = CTGAN(epochs=10)
    
    # Fit the model on the data
    ctgan_model.fit(data, discrete_columns)
    
    # Save the model to disk
    with open(model_path, 'wb') as f:
        pickle.dump(ctgan_model, f)


def sample_data(model_path='syntheticDataModel.pkl', num_samples=1000):
    # Load the model from disk
    with open(model_path, 'rb') as f:
        ctgan_model = pickle.load(f)
    
    # Generate synthetic data
    synthetic_data = ctgan_model.sample(num_samples)
    
    return synthetic_data

@app.route('/fit', methods=['POST'])
def api_fit_model():
    # Load data from local file

    logging.info("Starting to read the data")
    data_path = "../data/output.csv"

    try: 
        data = []
        with open(data_path, 'r') as file:
            for line in file:
                data.append(json.loads(line)['users'])
                logging.info(f"Read line from file: {line}")
        real_data = pd.DataFrame(data)
        logging.info(f"Starting the fit with data loaded from: {data_path}")
    except Exception as e:
        logging.error(f"Failed to load data: {str(e)}")
        return jsonify({"error": f"Failed to load data: {str(e)}"}), 500
    
    # Define discrete columns
    discrete_columns = ['id', 'first_name', 'last_name', 'street_address', 'city', 'state','zipcode', 'loyalty_plan']
    
    try:
        fit_model(real_data, discrete_columns)
        logging.info("Model training completed successfully")
        return jsonify({"message": "Model trained and saved successfully"})
    except Exception as e:
        logging.info("Model training failed successfully")
        return jsonify({"error": f"Error during model fitting: {str(e)}"}), 500

@app.route('/sample', methods=['GET'])
def api_sample_data():
    num_samples = request.args.get('samples', default=100, type=int)

    # Sample the model
    data = sample_data(num_samples=num_samples)

    synthetic_data = sample_data()
    print(synthetic_data)

    data_dict = data.to_dict(orient='records')
    return data_dict

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
