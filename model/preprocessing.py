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

def get_start_station(row):
    stations = {
        "DAR": 0,
        "BHM": 1
    }
    return stations[row['start_station']]

def get_end_station(row):
    stations = {
        "DAR": 0,
        "BHM": 1
    }
    return stations[row['end_station']]

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

def formatted_date_to_datetime(date : str) -> datetime.datetime:
    """
    Given a date in the format YYYY-MM-DD, return a datetime object representing the same date.
    """
    datee = datetime.datetime.strptime(date, "%Y-%m-%d")

    return datee

def encode_sin_date(date):
    datee = formatted_date_to_datetime(date)
    first_day_of_year = datetime.datetime(datee.year, 1, 1)

    num_days = abs((datee-first_day_of_year).days)

    return np.sin((2*np.pi*num_days)/365)

def encode_cos_date(date):
    datee = formatted_date_to_datetime(date)
    first_day_of_year = datetime.datetime(datee.year, 1, 1)

    num_days = abs((datee-first_day_of_year).days)

    return np.cos((2*np.pi*num_days)/365)

def encode_delay(delay):
    if delay >= 5:
        return True
    else:
        return False

def prepare_for_delay_classification(start_station, end_station):
    """
    Load Dataframe, remove irrelevant columns, encode date and time data.
    """
    fp = f"../data_collection/data/{start_station.lower()}_to_{end_station.lower()}_weather.csv"

    data = pd.read_csv(fp) 

    data = data.loc[lambda df: df['cancelled'] == False] # Not Cancelled Trains
    data = data.dropna(subset=['start_pta', 'start_ptd'], how='any')


   
    data['start_station'] = data.apply(get_start_station, axis=1) # Encode Start Station
    data['end_station'] = data.apply(get_end_station, axis=1) # Encode End Station

    #Date Encoding
    data['day_of_year_sin'] = [encode_sin_date(date) for date in data['date']]
    data['day_of_year_cos'] = [encode_cos_date(date) for date in data['date']]

    #Month Encoding
    data['month_sin'] = [encode_sin_month(month) for month in data['month']]
    data['month_cos'] = [encode_cos_month(month) for month in data['month']]


    #Month Encoding
    data['day_sin'] = [encode_sin_day_of_week(day) for day in data['day']]
    data['day_cos'] = [encode_cos_day_of_week(day) for day in data['day']]


    #Encoding time of day

    data['init_ptd_sin'] = [encode_sin_hour_minute(str(time)) for time in data['init_ptd']]
    data['init_ptd_cos'] = [encode_cos_hour_minute(str(time)) for time in data['init_ptd']]

    data['start_pta_sin'] = [encode_sin_hour_minute(str(time)) for time in data['start_pta']]
    data['start_pta_cos'] = [encode_cos_hour_minute(str(time)) for time in data['start_pta']]
    
#    data['start_ptd_sin'] = [encode_sin_hour_minute(time) for time in data['start_ptd']]
#    data['start_ptd_cos'] = [encode_cos_hour_minute(time) for time in data['start_pta']]


    data['end_pta_sin'] = [encode_sin_hour_minute(str(time)) for time in data['end_pta']]
    data['end_pta_cos'] = [encode_cos_hour_minute(str(time)) for time in data['end_pta']]
    

    data['actually_delayed'] = [encode_delay(delay) for delay in data['end_delay']]

    data = data.drop(['date', 'canc_reason', 'month', 'day','init_ptd', 'init_station', 'start_pta','start_ptd','end_pta','cancelled', 'toc_code', 'rid', 'canc_reason', 'start_ata', 'start_arrival_delay', 'start_dept_delay', 'init_atd', 'start_atd', 'start_dept_delay', 'end_ata', 'end_delay', 'delayed'], axis=1)

    return data


if __name__ == '__main__':
    data = prepare_for_delay_classification("dar", "bhm")


