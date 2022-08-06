from cmath import exp
import batch
from datetime import datetime
import pandas as pd


def dt(hour, minute, second=0):
    return datetime(2021, 1, 1, hour, minute, second)


def test_prepara_data():

    data = [
    (None, None, dt(1, 2), dt(1, 10)),
    (1, 1, dt(1, 2), dt(1, 10)),
    (1, 1, dt(1, 2, 0), dt(1, 2, 50)),
    (1, 1, dt(1, 2, 0), dt(2, 2, 1)),        
    ]

    columns = ['PUlocationID', 'DOlocationID', 'pickup_datetime', 'dropOff_datetime']
    df = pd.DataFrame(data, columns=columns)

    categorical = ['PUlocationID', 'DOlocationID']

    actual_result = batch.prepara_data(df,categorical)

    expected_data = [
    (str(-1), str(-1), dt(1, 2), dt(1, 10), (dt(1, 10) - dt(1, 2)).total_seconds() / 60),
    (str(1),str(1), dt(1, 2), dt(1, 10), (dt(1, 10) - dt(1, 2)).total_seconds() / 60),        
    ]

    expected_columns = ['PUlocationID', 'DOlocationID', 'pickup_datetime', 'dropOff_datetime','duration']

    expected_result = pd.DataFrame(expected_data,columns=expected_columns)


    pd.testing.assert_frame_equal(actual_result,expected_result)
    #assert actual_result==expected_result 
