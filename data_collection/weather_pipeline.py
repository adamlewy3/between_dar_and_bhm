"""

    The last step of data collection. The goal of this program is to take in a csv file of the form
    '{start_station}_to_{end_station}.csv' and adjoin weather data.

"""

# Core Imports
import csv
import pandas as pd
import os

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

def transform_and_load_csv(train_data : pd.DataFrame, start_station: str, end_station : str) -> None:
    """
    For each row in train_data, extract the row, turn it into a list, call for weather data, append the weather data, and load into a new csv. 
    """
    
    fp = f"data/{start_station.lower()}_to_{end_station.lower()}_weather.csv"

    num_rows = train_data.shape[0]

    for index, row in train_data.iterrows():
        date = row['date']

        #Info about the initial station
        init_station = row['init_station'] 

        if row['init_ptd']:
            init_ptd = str(row['init_ptd'])
            init_weather_station = utils.get_closest_weather_station(init_station)
            time = utils.string_time_to_formatted(date, init_ptd)
            init_weather_info = utils.hourly_weather(init_weather_station, time)
    



        #Info about the start station
        start_station = row['start_station']
        start_ptd = str(row['start_pta'])

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

        complete_weather_data = row.values.flatten().tolist() + init_weather_info + start_weather_info + end_weather_info

        #Load into new CSV

        if not os.path.exists(fp):
            columns =  [['rid','toc_code','date','month','day','cancelled','canc_reason','init_station','init_ptd','init_atd','start_station','start_pta','start_ata',"start_arrival_delay","start_ptd","start_atd","start_dept_delay","distance_from_init","end_station","end_pta","end_ata","end_delay","delayed", 'init_temp','init_rhum','init_prcp','init_snwd','init_wdir','init_wspd','init_wpgt','init_pres','init_tsun','init_cldc','init_coco','start_temp','start_rhum','start_prcp','start_snwd','start_wdir','start_wspd','start_wpgt','start_pres','start_tsun','start_cldc','start_coco','end_temp','end_rhum','end_prcp','end_snwd','end_wdir','end_wspd','end_wpgt','end_pres','end_tsun','end_cldc','end_coco']]
            file = open(fp, 'a', newline='')
            writer = csv.writer(file, lineterminator = '\n')
            writer.writerows(columns)
            print(f"Created file {fp}!")
            writer.writerows([complete_weather_data])
            print(f"Successfully written to {fp}! ({index+1}/{num_rows})")
        else:
            file = open(fp, 'a', newline='')
            writer = csv.writer(file, lineterminator = '\n')
            writer.writerows([complete_weather_data])
            print(f"Successfully written to {fp}! ({index+1}/{num_rows})")




if __name__ == '__main__':
    x = extract_csv("dar","bhm")
    transform_and_load_csv(x, "dar", "bhm")
