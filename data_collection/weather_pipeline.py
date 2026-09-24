"""

    The last step of data collection. The goal of this program is to take in a csv file of the form
    '{start_station}_to_{end_station}.csv' and adjoin weather data.

"""

# Core Imports
import csv
import pandas as pd

# Internal Imports
import utils

#External Imports 
import meteostat as ms

def extract_csv(start_station: str, end_station: str) -> None | pd.DataFrame:
    """
    Open and load our desired csv file into a pandas dataframe.
    """
    fp = f"data/{start_station.lower()}_to_{end_station.lower()}.csv"

    try:
        df = pd.read_csv(fp)
    except:
        print(f"File '{fp}' does not exist!")
        return None

    df = pd.read_csv(fp)
    return df

def transform_and_load_csv(train_data : pd.DataFrame) -> None:
    """
    For each row in train_data, extract the row, turn it into a list, call for weather data, append the weather data, and load into a new csv. 
    """
    for index, row in train_data.iterrows():
        date = row['date']

        #Info about the initial station
        init_station = row['init_station'] 
        init_ptd = str(row['init_ptd'])

        # Getting weather data

        init_weather_station = utils.get_closest_weather_station(init_station)
        time = utils.string_time_to_formatted(date, init_ptd)
        init_weather_info = utils.hourly_weather(init_weather_station, time)


        #Info about the start station
        start_station = row['start_station']
        start_ptd = str(row['start_ptd'])

        start_weather_station = utils.get_closest_weather_station(start_station)
        time = utils.string_time_to_formatted(date, start_ptd)
        start_weather_info = utils.hourly_weather(start_weather_station, time)

        #Info about the end station
        end_station = row['end_station']
        end_pta = str(row['end_pta'])

        end_weather_station = utils.get_closest_weather_station(end_station)
        time = utils.string_time_to_formatted(date, end_pta)
        end_weather_info = utils.hourly_weather(end_weather_station, time)

        # Get weather data

        complete_weather_data = init_weather_info + start_weather_info + end_weather_info

        print(complete_weather_data)
        #Load into new CSV




if __name__ == '__main__':
    x = extract_csv("dar","bhm")
    transform_and_load_csv(x)
