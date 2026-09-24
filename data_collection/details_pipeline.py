"""

    Data Pipeline for a specific train with a given RID.

"""

#Core Imports
import json 
import csv
import datetime 
import time 
import os

#Internal Imports
import utils

#External Imports
import requests
from dotenv import load_dotenv

load_dotenv()

headers = {
    "User-Agent": "",
    "Content-Type": "application/json",
    "x-apikey": os.getenv("APIKEY") 
}

reqUrl = os.getenv("DETAILS_URL")

# Load RID
def load_rids(date : datetime.datetime, start_station: str, end_station: str):
    """
    Given a datetime object, return all RIDS of trains from that day from start_station to end_station
    """
    filepath = f"data/rids_{start_station.lower()}_to_{end_station.lower()}.json"

    formatted_date = utils.format_date(date)
    
    with open(filepath) as file:
        info = json.load(file)
        rids = info[formatted_date]
        if rids is not None:
            return rids


def get_details(rid : str, write =False):
    payload = json.dumps({
        'rid':rid
    })

    print(f"Sending HTTP Post Request for RID {rid}.") 
    
    t0 = time.time()
    response = requests.request("POST", reqUrl, data=payload, headers = headers) 
    t1 = time.time()
    #Check if this works

    print(f"Status code {response.status_code} received after {t1-t0:.2f} seconds")

    if response.status_code == 200 and write == False:
        return response.json()
    elif response.status_code == 200 and write == True:
        fp = f"testdata/{rid}.json"
        with open(fp, 'w') as file:
            json.dump(response.json(), file, indent=2)
            file.close()

    else:
        print(f"Failed to get details of service with RID {rid}.") 

def transform_details(body : dict, start_station: str, end_station: str):
    """
    Given the json input (as a python dictionary), extract the data that we would like. (Transform the response from the HTTP server)
    """
    # Operational Information

    date = body["serviceAttributesDetails"]["date_of_service"] #String in the form YYYY-MM-DD
    toc_code = body["serviceAttributesDetails"]["toc_code"]
    rid = body["serviceAttributesDetails"]["rid"]
    datee = utils.formatted_date_to_datetime(date)
    month = utils.get_month(datee)
    day = utils.get_weekday(datee)


    # Get Locations

    locations = body["serviceAttributesDetails"]["locations"] #List of dictionaries

    init_location = locations[0]

    start_location = utils.get_location(locations, start_station)
    end_location = utils.get_location(locations, end_station)


    # Check For Cancellation 
    cancelled = utils.is_cancelled(start_location, end_location) 

    #Check for cancellation/lateness reason
    canc_reason = utils.late_canc_reason(start_location, end_location, cancelled)

    operational_info = [rid, toc_code, date, month, day, cancelled, canc_reason]

    # --- Initial Station Info --- 
    init_station, init_ptd, init_atd = utils.init_punc_details(init_location, cancelled)
    
    init_station_info = [init_station, init_ptd, init_atd]

    # --- Start Station Info --- 
    start_station, start_pta, start_ata, start_arrival_delay, start_ptd, start_atd, start_dept_delay = utils.start_punc_details(start_location, cancelled) 

    start_station_info = [start_station, start_pta, start_ata, start_arrival_delay, start_ptd, start_atd, start_dept_delay, utils.distance_between_stations(init_station, start_station)]

    # --- End Station Info --- 

    end_station, end_pta, end_ata, end_delay, delayed = utils.end_punc_details(end_location, cancelled)

    end_station_info = [end_station, end_pta, end_ata, end_delay, delayed]


    return [operational_info + init_station_info + start_station_info + end_station_info]


def load_details(data, start_station, end_station):
    """
    Given the result of transform_details, append to the csv 'data/{start_station}_to_{end_station}.csv'
    """
    fp = f"data/{start_station.lower()}_to_{end_station.lower()}.csv"
    if not os.path.exists(fp):
        file = open(fp, 'a', newline='')
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows([['rid','toc_code','date','month','day','cancelled','canc_reason','init_station','init_ptd','init_atd','start_station','start_pta','start_ata','start_arrival_delay','start_ptd','start_atd','start_dept_delay','distance_from_init','end_station','end_pta','end_ata','end_delay','delayed']])
        print(f"Created file")
        writer.writerows(data)
        print(f"Successfully written to {fp}!")
        file.close()
    else:
        file = open(fp, 'a', newline='')
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows(data)
        print(f"Succesfully Written to {fp}!")
        file.close()
        


"""
Format of the file '{start_station}_to_{end_station}.csv'

Columns: 

--- Operational Info --- 
rid: The Unique Identifying Number of the Train
toc_code: The TOC Code of the train provider.
date: In the form YYYY-MM-DD
month: In words, e.g. JAN, FEB, MAR, etc.
day: In words, e.g. MON, TUE, WED, etc. 
cancelled: Boolean, whether the train was cancelled (NOT (departed from start_station OR arrived at end_station)
canc_reason : 3-digit Code giving late/cancellation reason, or None, if there is no reason.

--- Initial Station Info ---
init_station: The train station where the service begins. (Different from the start_station!)
init_ptd: The initial ptd (predicted time of departure) in the format HHMM
init_atd: The initial atd (actual time of departure) in the format HHMM

--- Start Station Info ---
start_station: The first station we care about 
start_pta: The predicted time of arrival at start_station
start_ata: The actual time of arrival at start_station
start_arrival_delay: The difference between start_ata and start_pta.
start_ptd: The ptd (predicted time of departure) from start_station.
start_atd: The atd (actual time of departure from start_station.
start_dept_delay: The difference between the start_atd and start_ptd
distance_from_init: The distance between the initial station and start_station (Just need a table for this)

--- End Station Info --- 
end_station: The ending station we care about 
end_pta: The predicted time of arrival at start_station
end_ata: The actual time of arrival at start_station
end_delay: The difference between start_ata and start_pta.
delayed: Bool, True if end_delay > 0. False if end_delay <= 0

The end goal is to use day of the week, time of day, month of the year, distance from initial station to predict train delays. Need to prove first that this is reasonable.

"""



if __name__ == '__main__':
    """
    Main Loop for the program
    """

    """
    start_station = "DAR"
    end_station = "BHM"
    initial_date = datetime.datetime(2026,2,28)
    for i in range(200):
        current_date = initial_date + datetime.timedelta(days=i)
        rids = load_rids(current_date, start_station, end_station)
        if rids is None or len(rids) == 0:
            continue
        else:
            for rid in rids:
                data = get_details(rid)
                transformed_data = transform_details(data, start_station, end_station)
                load_details(transformed_data, start_station, end_station)
    """


