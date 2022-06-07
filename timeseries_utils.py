import pandas as pd
from datetime import datetime, timedelta

def generate_dataframe(date, prediction):
    zero_week = datetime.now()
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
