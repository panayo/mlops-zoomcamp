#!/usr/bin/env python
# coding: utf-8


import pickle
import pandas as pd
import numpy as np
from datetime import datetime
import sys



with open('model.bin', 'rb') as f_in:
    dv, lr = pickle.load(f_in)

def apply_model(year,month):
    df = pd.read_parquet(f'https://nyc-tlc.s3.amazonaws.com/trip+data/fhv_tripdata_{year:04d}-{month:02d}.parquet')
    categorical = ['PUlocationID', 'DOlocationID']
    
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)
    pred_mean = np.round(np.mean(y_pred),2)
    return y_pred,pred_mean


def save_result(df,y_pred):

    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predicted_duration'] = y_pred
    output_file = f'data/predictions_fhv_tripdata_{year:04d}-{month:02d}.parquet'

    df_result.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False
    )


def run():
    year = int(sys.argv[1]) #2021
    month = int(sys.argv[2]) # 3

    y_pred,pred_mean = apply_model(month=month,year=year)
    print(pred_mean)

if __name__ == '__main__':
    run()






    