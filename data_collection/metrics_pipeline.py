"""

    Data Pipeline giving the RID's of all desired services.

"""

# Core Imports

import json
import time
import datetime
import os

# External Imports

import requests 

# Internal Imports

import utils
from dotenv import load_dotenv


# Information that remains constant with every request.

START_STATION = "DAR"
END_STATION = "BHM"

load_dotenv()

headers = {
    "User-Agent": "",
    "Content_Type" : "application/json",
    "x-apikey": os.getenv("APIKEY")
}

reqUrl = os.getenv("METRICS_URL") 
# Preparing the payload

def get_weekday_payload(date: datetime.datetime) -> str:
    """
    Given a datetime object, return the appropriate string represenattion of the date for the payload.
    """
    day = date.weekday()

    if day < 5:
        return "WEEKDAY"
    elif day == 5:
        return "SATURDAY"
    else:
        return "SUNDAY"
    # TODO: Write Tests for These

def get_initial_datetime(date: datetime.datetime) -> datetime.datetime:
    """
    Given a datetime object, return the same date at 5am, which is the point from which we will start collecitng RIDs.
    """
    return datetime.datetime(year = date.year, month = date.month, day = date.day, hour = 5, minute = 00)
    #TODO: Write Tests for These

def format_time(date: datetime.datetime) -> str:
    """
    Given a datetime object, return str HH:MM
    """
    time_format = "%H%M"
    return date.strftime(time_format)


"""
    Format of the file 'rids.json'
    {
        date1 : ['rid1', 'rid2', ..],
        date2 : ['rid1', 'rid2', ..],
        ...
    }
"""

def get_rids(date : datetime.datetime, start_station : str, end_station : str) -> list[str] | None:
    """
    Returns a list of all RIDs of all trains that ran in a day from start_station to end_station. Append to the json file of RIDs
    """
    date = get_initial_datetime(date)
    formatted_date = utils.format_date(date)
    formatted_day = get_weekday_payload(date) 

    res = []
    
    for i in range(18): #None of the services I want to investigate run during the night. This is 5am to 11pm
        #Preparing the payload
        from_time = format_time(date + datetime.timedelta(hours=i))
        to_time = format_time(date + datetime.timedelta(hours=i+1))
        payload = json.dumps({
            "from_loc" : start_station,
            "to_loc" : end_station,
            "from_time" : from_time,
            "to_time" : to_time,
            "from_date" : formatted_date,
            "to_date" : formatted_date,
            "days" : formatted_day
        })

        print("Sending HTTP Post Request")
        t0 = time.time()
        reqUrl = os.getenv("METRICS_URL") 
        response = requests.request("POST", reqUrl, data=payload, headers=headers)
        t1 = time.time()

        status_code = response.status_code

        if status_code != 200:
            # Handling Bad Response. Ending Loop Here So I know which Day I'm on.
            print(f"HTTP Post Request Failed after {t1-t0:.2f} seconds, failed on day {formatted_date}")
            print(f"{status_code}")
            return None
        else:
            print(f"HTTP Post Request Succeeded after {t1-t0:.2f} seconds.")
            if len(response.json()["Services"]) == 0: # Handing the case when no services ran
                print(f"No services ran between {from_time} and {to_time}.")
                print(f"Waiting 1 second to send next request.")
                time.sleep(1)
            else:
                rids = response.json()["Services"][0]["serviceAttributesMetrics"]["rids"] 
                for rid in rids:
                    res.append(rid)

                print(f"Found RID's of services between {from_time} and {to_time}.")
                print(f"Waiting 1 second to send next request.")
                time.sleep(1)

    return res 

def append_rids(date, res):

    with open("data/rids_dar_to_bhm.json", 'r') as file:
        info = json.load(file)

    info[utils.format_date(date)] = res 


    with open("data/rids_dar_to_bhm.json", 'w') as file:
        json.dump(info, file, indent=2)
        print("Successfully written to 'data/rids_dar_to_bhm.json'!")

    
if __name__ == '__main__':
    # Get RIDs from the past year
    initial_date = datetime.datetime(2026,4, 7)

    get_rids(initial_date, "DAR", "BHM")

