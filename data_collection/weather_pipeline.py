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
from tqdm import tqdm

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

    for index, row in tqdm(train_data.iterrows(), desc='Compiling Weather Data'):
        date = row['date']

        if not row['cancelled']:
            #Info about the initial station
            init_station = row['init_station'] 


            init_ptd = str(row['init_ptd'])
            init_weather_station = utils.get_closest_weather_station(init_station)
            time = utils.string_time_to_formatted(date, init_ptd)
            init_weather_info = utils.hourly_weather(init_weather_station, time)

            init_12_hour = utils.weather_lookback_avg(init_weather_station, time, 12)
            init_24_hour = utils.weather_lookback_avg(init_weather_station, time, 24)
            init_72_hour = utils.weather_lookback_avg(init_weather_station, time, 72)


            #Info about the start station
            start_station = row['start_station']
            start_ptd = str(row['start_ptd'])

            start_weather_station = utils.get_closest_weather_station(start_station)
            time = utils.string_time_to_formatted(date, start_ptd)
            start_weather_info = utils.hourly_weather(start_weather_station, time)

            #12/24/72hr Rolling AVG for start_station

            start_12_hour = utils.weather_lookback_avg(start_weather_station, time, 12)
            start_24_hour = utils.weather_lookback_avg(start_weather_station, time, 24)
            start_72_hour = utils.weather_lookback_avg(start_weather_station, time, 72)
            

            #Info about the end station
            end_station = row['end_station']
            end_pta = str(row['end_pta'])

            end_weather_station = utils.get_closest_weather_station(end_station)
            time = utils.string_time_to_formatted(date, end_pta)
            end_weather_info = utils.hourly_weather(end_weather_station, time)

            #12/24/72hr Rolling AVG for end_station

            end_12_hour = utils.weather_lookback_avg(end_weather_station, time, 12)
            end_24_hour = utils.weather_lookback_avg(end_weather_station, time, 24)
            end_72_hour = utils.weather_lookback_avg(end_weather_station, time, 72)

            # Get weather data

            complete_weather_data = row.values.flatten().tolist() + init_weather_info + init_12_hour + init_24_hour + init_72_hour + start_weather_info + start_12_hour + start_24_hour + start_72_hour + end_weather_info+ end_12_hour + end_24_hour + end_72_hour

        #Load into new CSV

            if not os.path.exists(fp):
                columns =  [['rid','toc_code','date','month','day','cancelled','canc_reason','init_station','init_ptd','init_atd','start_station','start_pta','start_ata',"start_arrival_delay","start_ptd","start_atd","start_dept_delay","distance_from_init","end_station","end_pta","end_ata","end_delay","delayed",
                             'init_temp','init_rhum','init_prcp','init_snwd','init_wdir','init_wspd','init_wpgt','init_pres','init_tsun','init_cldc','init_coco', 
                             'init_12_mean_temp', 'init_12_min_temp', 'init_12_max_temp', 'init_12_mean_wspd', 'init_12_min_wspd', 'init_12_max_wspd', 'init_12_mean_rhum','init_12_min_rhum', 'init_12_max_rhum', 'init_12_mean_pres', 'init_12_min_pres', 'init_12_max_pres', 'init_12_mean_prcp', 'init_12_cum_prcp', 
                             'init_24_mean_temp', 'init_24_min_temp', 'init_24_max_temp', 'init_24_mean_wspd', 'init_24_min_wspd', 'init_24_max_wspd', 'init_24_mean_rhum','init_24_min_rhum', 'init_24_max_rhum', 'init_24_mean_pres', 'init_24_min_pres', 'init_24_max_pres', 'init_24_mean_prcp', 'init_24_cum_prcp', 
                             'init_72_mean_temp', 'init_72_min_temp', 'init_72_max_temp', 'init_72_mean_wspd', 'init_72_min_wspd', 'init_72_max_wspd', 'init_72_mean_rhum','init_72_min_rhum', 'init_72_max_rhum', 'init_72_mean_pres', 'init_72_min_pres', 'init_72_max_pres', 'init_72_mean_prcp', 'init_72_cum_prcp', 
                             'start_temp','start_rhum','start_prcp','start_snwd','start_wdir','start_wspd','start_wpgt','start_pres','start_tsun','start_cldc','start_coco',
                            'start_12_mean_temp', 'start_12_min_temp', 'start_12_max_temp', 'start_12_mean_wspd', 'start_12_min_wspd', 'start_12_max_wspd', 'start_12_mean_rhum','start_12_min_rhum', 'start_12_max_rhum', 'start_12_mean_pres', 'start_12_min_pres', 'start_12_max_pres', 'start_12_mean_prcp', 'start_12_cum_prcp', 
                             'start_24_mean_temp', 'start_24_min_temp', 'start_24_max_temp', 'start_24_mean_wspd', 'start_24_min_wspd', 'start_24_max_wspd', 'start_24_mean_rhum','start_24_min_rhum', 'start_24_max_rhum', 'start_24_mean_pres', 'start_24_min_pres', 'start_24_max_pres', 'start_24_mean_prcp', 'start_24_cum_prcp', 
                             'start_72_mean_temp', 'start_72_min_temp', 'start_72_max_temp', 'start_72_mean_wspd', 'start_72_min_wspd', 'start_72_max_wspd', 'start_72_mean_rhum','start_72_min_rhum', 'start_72_max_rhum', 'start_72_mean_pres', 'start_72_min_pres', 'start_72_max_pres', 'start_72_mean_prcp', 'start_72_cum_prcp', 
                             'end_temp','end_rhum','end_prcp','end_snwd','end_wdir','end_wspd','end_wpgt','end_pres','end_tsun','end_cldc','end_coco',
                            'end_12_mean_temp', 'end_12_min_temp', 'end_12_max_temp', 'end_12_mean_wspd', 'end_12_min_wspd', 'end_12_max_wspd', 'end_12_mean_rhum','end_12_min_rhum', 'end_12_max_rhum', 'end_12_mean_pres', 'end_12_min_pres', 'end_12_max_pres', 'end_12_mean_prcp', 'end_12_cum_prcp', 
                             'end_24_mean_temp', 'end_24_min_temp', 'end_24_max_temp', 'end_24_mean_wspd', 'end_24_min_wspd', 'end_24_max_wspd', 'end_24_mean_rhum','end_24_min_rhum', 'end_24_max_rhum', 'end_24_mean_pres', 'end_24_min_pres', 'end_24_max_pres', 'end_24_mean_prcp', 'end_24_cum_prcp', 
                             'end_72_mean_temp', 'end_72_min_temp', 'end_72_max_temp', 'end_72_mean_wspd', 'end_72_min_wspd', 'end_72_max_wspd', 'end_72_mean_rhum','end_72_min_rhum', 'end_72_max_rhum', 'end_72_mean_pres', 'end_72_min_pres', 'end_72_max_pres', 'end_72_mean_prcp', 'end_72_cum_prcp']]
                file = open(fp, 'a', newline='')
                writer = csv.writer(file, lineterminator = '\n')
                writer.writerows(columns)
                print(f"Created file {fp}!")
                writer.writerows([complete_weather_data])
            else:
                file = open(fp, 'a', newline='')
                writer = csv.writer(file, lineterminator = '\n')
                writer.writerows([complete_weather_data])
        else:
            if not os.path.exists(fp):
                columns =  [['rid','toc_code','date','month','day','cancelled','canc_reason','init_station','init_ptd','init_atd','start_station','start_pta','start_ata',"start_arrival_delay","start_ptd","start_atd","start_dept_delay","distance_from_init","end_station","end_pta","end_ata","end_delay","delayed",
                             'init_temp','init_rhum','init_prcp','init_snwd','init_wdir','init_wspd','init_wpgt','init_pres','init_tsun','init_cldc','init_coco', 
                             'init_12_mean_temp', 'init_12_min_temp', 'init_12_max_temp', 'init_12_mean_wspd', 'init_12_min_wspd', 'init_12_max_wspd', 'init_12_mean_rhum','init_12_min_rhum', 'init_12_max_rhum', 'init_12_mean_pres', 'init_12_min_pres', 'init_12_max_pres', 'init_12_mean_prcp', 'init_12_cum_prcp', 
                             'init_24_mean_temp', 'init_24_min_temp', 'init_24_max_temp', 'init_24_mean_wspd', 'init_24_min_wspd', 'init_24_max_wspd', 'init_24_mean_rhum','init_24_min_rhum', 'init_24_max_rhum', 'init_24_mean_pres', 'init_24_min_pres', 'init_24_max_pres', 'init_24_mean_prcp', 'init_24_cum_prcp', 
                             'init_72_mean_temp', 'init_72_min_temp', 'init_72_max_temp', 'init_72_mean_wspd', 'init_72_min_wspd', 'init_72_max_wspd', 'init_72_mean_rhum','init_72_min_rhum', 'init_72_max_rhum', 'init_72_mean_pres', 'init_72_min_pres', 'init_72_max_pres', 'init_72_mean_prcp', 'init_72_cum_prcp', 
                             'start_temp','start_rhum','start_prcp','start_snwd','start_wdir','start_wspd','start_wpgt','start_pres','start_tsun','start_cldc','start_coco',
                            'start_12_mean_temp', 'start_12_min_temp', 'start_12_max_temp', 'start_12_mean_wspd', 'start_12_min_wspd', 'start_12_max_wspd', 'start_12_mean_rhum','start_12_min_rhum', 'start_12_max_rhum', 'start_12_mean_pres', 'start_12_min_pres', 'start_12_max_pres', 'start_12_mean_prcp', 'start_12_cum_prcp', 
                             'start_24_mean_temp', 'start_24_min_temp', 'start_24_max_temp', 'start_24_mean_wspd', 'start_24_min_wspd', 'start_24_max_wspd', 'start_24_mean_rhum','start_24_min_rhum', 'start_24_max_rhum', 'start_24_mean_pres', 'start_24_min_pres', 'start_24_max_pres', 'start_24_mean_prcp', 'start_24_cum_prcp', 
                             'start_72_mean_temp', 'start_72_min_temp', 'start_72_max_temp', 'start_72_mean_wspd', 'start_72_min_wspd', 'start_72_max_wspd', 'start_72_mean_rhum','start_72_min_rhum', 'start_72_max_rhum', 'start_72_mean_pres', 'start_72_min_pres', 'start_72_max_pres', 'start_72_mean_prcp', 'start_72_cum_prcp', 
                             'end_temp','end_rhum','end_prcp','end_snwd','end_wdir','end_wspd','end_wpgt','end_pres','end_tsun','end_cldc','end_coco',
                            'end_12_mean_temp', 'end_12_min_temp', 'end_12_max_temp', 'end_12_mean_wspd', 'end_12_min_wspd', 'end_12_max_wspd', 'end_12_mean_rhum','end_12_min_rhum', 'end_12_max_rhum', 'end_12_mean_pres', 'end_12_min_pres', 'end_12_max_pres', 'end_12_mean_prcp', 'end_12_cum_prcp', 
                             'end_24_mean_temp', 'end_24_min_temp', 'end_24_max_temp', 'end_24_mean_wspd', 'end_24_min_wspd', 'end_24_max_wspd', 'end_24_mean_rhum','end_24_min_rhum', 'end_24_max_rhum', 'end_24_mean_pres', 'end_24_min_pres', 'end_24_max_pres', 'end_24_mean_prcp', 'end_24_cum_prcp', 
                             'end_72_mean_temp', 'end_72_min_temp', 'end_72_max_temp', 'end_72_mean_wspd', 'end_72_min_wspd', 'end_72_max_wspd', 'end_72_mean_rhum','end_72_min_rhum', 'end_72_max_rhum', 'end_72_mean_pres', 'end_72_min_pres', 'end_72_max_pres', 'end_72_mean_prcp', 'end_72_cum_prcp']]
                columns =  [['rid','toc_code','date','month','day','cancelled','canc_reason','init_station','init_ptd','init_atd','start_station','start_pta','start_ata',"start_arrival_delay","start_ptd","start_atd","start_dept_delay","distance_from_init","end_station","end_pta","end_ata","end_delay","delayed", 'init_temp','init_rhum','init_prcp','init_snwd','init_wdir','init_wspd','init_wpgt','init_pres','init_tsun','init_cldc','init_coco','start_temp','start_rhum','start_prcp','start_snwd','start_wdir','start_wspd','start_wpgt','start_pres','start_tsun','start_cldc','start_coco','end_temp','end_rhum','end_prcp','end_snwd','end_wdir','end_wspd','end_wpgt','end_pres','end_tsun','end_cldc','end_coco']]
                file = open(fp, 'a', newline='')
                writer = csv.writer(file, lineterminator = '\n')
                writer.writerows(columns)
                writer.writerows([row])
            else:
                file = open(fp, 'a', newline='')
                writer = csv.writer(file, lineterminator = '\n')
                writer.writerows([row])



            # We are not interested in cancelled trains, so 
            

            # Train is cancelled, so load into empty csv.




if __name__ == '__main__':
    x = extract_csv("dar","bhm")
    transform_and_load_csv(x, "dar", "bhm")
