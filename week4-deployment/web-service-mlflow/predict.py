import os
import pickle

import mlflow
from flask import Flask, request, jsonify
from mlflow.tracking import MlflowClient


# run id with dv and model separately (without pipeline)
# RUN_ID = '7f5a0fcf927d4aafa435cc78ae453357'

# run id with pipeline
# RUN_ID = 'a830f9c286644b3989d782ecc939d4d1'

# run id id as environment variable (run id with pipeline)
RUN_ID = os.getenv('RUN_ID')
# dependency with the tracking server

# MLFLOW_TRACKING_URI = 'http://127.0.0.1:5000'
# mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
# logged_model = f'runs:/{RUN_ID}/model'

# without dependency of tracking server
# local  
# logged_model = f"./mlruns/1/{RUN_ID}/artifacts/model"

# on S3
logged_model = f's3://mlflow-artifacts-remote-store/2/{RUN_ID}/artifacts/model'


model = mlflow.pyfunc.load_model(logged_model)

# load DictVectorizer with the run id with artifact

# client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)

# path = client.download_artifacts(run_id=RUN_ID, path='dict_vectorizer.bin')
# print(f'downloading the dict vectorize to {path}')

# with open(path, 'rb') as f_out:
#     dv = pickle.load(f_out)



def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features


def predict(features):
    # with the run id with artifact
    # X = dv.tansform(features)
    # preds = model.predict(X)
    preds = model.predict(features)
    return float(preds[0])


app = Flask('duration-prediction')


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()

    features = prepare_features(ride)
    pred = predict(features)

    result = {
        'duration': pred,
        'model_version': RUN_ID
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
