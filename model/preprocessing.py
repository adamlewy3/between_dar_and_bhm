import pandas as pd
import numpy as np
import datetime

def string_time_to_formatted(time : str) -> datetime.datetime:
    """
    Given a time in the form HHMM, return a datetime object with hour HH and minute MM
    """
    time = time.split('.')[0] 

    if len(time) == 3 or (len(time) == 4 and time[0] == "0"):
        hour = int(time[0])
        minutes = int(time[1:3])
        return datetime.datetime(2025, 10, 1, hour, minutes)
    else:
        hour = int(time[0:2])
        minutes = int(time[2:4])
        return datetime.datetime(2025, 10, 1, hour, minutes)

def get_station(station):
    stations = {
        "DAR": 0,
        "BHM": 1
    }
    return stations[station]

def encode_sin_hour_minute(time):
    datee = string_time_to_formatted(time)

    hour = datee.hour
    minute = datee.minute

    time_new = hour + (minute/60)

    return np.sin((2*np.pi*time_new)/24)

def encode_cos_hour_minute(time):
    time = str(time)
    datee = string_time_to_formatted(time)

    hour = datee.hour
    minute = datee.minute

    time_new = hour + (minute/60)

    return np.cos((2*np.pi*time_new)/24)

def encode_sin_day_of_week(day):
    days = {
        "MON" : 1,
        "TUE" : 2,
        "WED" : 3,
        "THU" : 4,
        "FRI" : 5,
        "SAT" : 6,
        "SUN" : 7
    }
    return np.sin((2*np.pi*days[day])/7)

def encode_cos_day_of_week(day):
    days = {
        "MON" : 1,
        "TUE" : 2,
        "WED" : 3,
        "THU" : 4,
        "FRI" : 5,
        "SAT" : 6,
        "SUN" : 7
    }
    return np.cos((2*np.pi*days[day])/7)

def encode_sin_month(month):
    months = {
        "JAN" : 1,
        "FEB" : 2,
        "MAR" : 3,
        "APR" : 4,
        "MAY" : 5,
        "JUN" : 6,
        "JUL" : 7,
        "AUG" : 8,
        "SEP" : 9,
        "OCT" : 10,
        "NOV" : 11,
        "DEC" : 12
    }
    return np.sin((2*np.pi*months[month])/12) 

def encode_cos_month(month):
    months = {
        "JAN" : 1,
        "FEB" : 2,
        "MAR" : 3,
        "APR" : 4,
        "MAY" : 5,
        "JUN" : 6,
        "JUL" : 7,
        "AUG" : 8,
        "SEP" : 9,
        "OCT" : 10,
        "NOV" : 11,
        "DEC" : 12
    }
    return np.cos((2*np.pi*months[month])/12) 

def prepare_for_delay_classification(start_station, end_station):
    """
    Load Dataframe, remove irrelevant columns, encode date and time data.
    """
    fp = f"data/{start_station.lower()}_to_{end_station.lower()}_weather.csv"

    data = pd.read_csv(fp)

    # Remove cancelled trains:
    pass

if __name__ == '__main__':
    train_data = pd.read_csv("cleaned_data/not_cancelled_trains_dar_to_bhm.csv")
    train_data['init_ptd'] = train_data['init_ptd'].apply(encode_cos_hour_minute)
    print(train_data['init_ptd'])
