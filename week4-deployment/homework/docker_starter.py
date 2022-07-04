from flask import Flask, request, jsonify
import numpy as np
import pickle
import pandas as pd
import numpy as np
import os 



def load_dic(file):
    with open(file, 'rb') as f_in:
        dv, lr = pickle.load(f_in)
    return dv,lr
    
def read_data(filename):
    df = pd.read_parquet(filename)
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    return df

def data_processing(year,month):

    df = read_data(f'https://nyc-tlc.s3.amazonaws.com/trip+data/fhv_tripdata_{year:04d}-{month:02d}.parquet')
    categorical = ['PUlocationID', 'DOlocationID']
    dv, lr = load_dic('model.bin')
    dicts = df[categorical].to_dict(orient='records')
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

    X_val = dv.transform(dicts)
    return lr,X_val,df

def predict(lr,X_val):
    y_pred = lr.predict(X_val)
    #pred_mean = np.round(np.mean(y_pred),2)
    return y_pred


def save_results(df,y_pred,output_file):
    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predicted_duration'] = y_pred
    df_result.to_parquet(output_file, index=False)


app = Flask('homework-week4')    
@app.route('/predict', methods=['POST'])
def end_point():

    date = request.get_json()

    year, month = date['year'], date['month']

    
    lr, X_val,df = data_processing(year, month)
    pred = predict(lr,X_val)
    output_file =  f'predictions_fhv_tripdata_{year:04d}-{month:02d}.parquet'
    save_results(df,pred,output_file)

    result = {
        'mean prediction': np.round(np.mean(pred),2)
    }
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)