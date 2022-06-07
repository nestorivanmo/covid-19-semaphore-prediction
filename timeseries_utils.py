import pandas as pd
from datetime import datetime, timedelta

def generate_dataframe(date, prediction):
    if date is None:
        zero_week = datetime.now()
    else:
        date_str = date[8:10] + date[5:7] + date[2:4]
        zero_week = datetime.strptime(date_str, '%d%m%y')
    two_weeks = zero_week + timedelta(days=14)
    four_weeks = zero_week + timedelta(days=30)
    eight_weeks = zero_week + timedelta(days=60)

    df = pd.DataFrame({
        'date' : [zero_week, two_weeks, four_weeks, eight_weeks],
        'semaphore' : prediction
    })
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    return df
