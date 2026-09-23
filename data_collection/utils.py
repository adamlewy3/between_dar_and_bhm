"""

    Utilities. Functions that are used in multiple programs (following DRY principle)

"""

#Core Imports 

import datetime 
import time
import json
import os
    
def get_weekday(date: datetime.datetime) -> str:
    """
    Given a datetime object, return the day of the week.
    """

    days_of_week = {
        0: "MON",
        1: "TUE",
        2: "WED",
        3: "THU",
        4: "FRI", 
        5: "SAT",
        6: "SUN"
    }

    day = date.weekday()

    return days_of_week[day]

def get_month(date: datetime.datetime) -> str:
    """
    Given a python datetime object, return the month as a string.
    """
    months = {
        1: "JAN",
        2: "FEB",
        3: "MAR",
        4: "APR",
        5: "MAY",
        6: "JUN",
        7: "JUL",
        8: "AUG",
        9: "SEP",
        10: "OCT",
        11: "NOV",
        12: "DEC"
    }

    return months[date.month]


def formatted_date_to_datetime(date : str) -> datetime.datetime:
    """
    Given a date in the format YYYY-MM-DD, return a datetime object representing the same date.
    """
    datee = datetime.datetime.strptime(date, "%Y-%m-%d")

    return datee

def format_date(date: datetime.datetime) -> str:
    """
    Given a datetime object, return str YYYY-MM-DD
    """

    date_format = "%Y-%m-%d"
    return date.strftime(date_format)

def get_delay(time1: str, time2: str) -> int | None:
    """
    Given times time1 and time2, in the format HHMM, return the difference.

    time1 is the expected time of arrival/departure, time2 is the actual time of arrival/departure
    """
    if time1 == "" or time2 == "":
        return None

    time1_hour = int(time1[0:2])
    time1_minutes = int(time1[2:4])
    time1_formatted = datetime.datetime(2025, 10, 1, hour=time1_hour, minute=time1_minutes)

    time2_hour = int(time2[0:2])
    time2_minutes = int(time2[2:4])
    if time2_hour >= time1_hour:
        time2_formatted = datetime.datetime(2025, 10 ,1, hour=time2_hour, minute=time2_minutes)
        minutes_diff = (time2_formatted - time1_formatted).total_seconds() // 60
        return int(minutes_diff)
    else:
        time_2_formatted = datetime.datetime(2025,10,2, hour=time2_hour, minute= time2_minutes)
        minutes_diff = (time2_formatted - time1_formatted).total_seconds() // 60
        return int(minutes_diff)

def get_location(locations: list[dict], station: str) -> dict: 
    """
    Given the list of dictionaries containing arrival info, return the information of the desired station.
    """
    for location in locations:
        if location["location"] == station:
            return location

def init_punc_details(location: dict, cancelled=False) -> Tuple:
    """
    Given a dictionary of the following form:
            {
                "location": "BWK",
                "gbtt_ptd": "1346",
                "gbtt_pta": "",
                "actual_td": "1346",
                "actual_ta": "",
                "late_canc_reason": ""
            }

    Return init_station, init_ptd, init_atd
    """
    if cancelled == True:
        init_station = location["location"]
        init_ptd = location["gbtt_ptd"]
        init_atd = None
        return init_station, init_ptd, init_atd
    else:
        init_station = location["location"]
        init_ptd = location["gbtt_ptd"]
        init_atd = location["actual_td"]
        return init_station, init_ptd, init_atd
        

def start_punc_details(location: dict, cancelled = False) -> Tuple:
    """
    Given a dictionary of the following form:
            {
                "location": "BWK",
                "gbtt_ptd": "1346",
                "gbtt_pta": "1345",
                "actual_td": "1346",
                "actual_ta": "1344",
                "late_canc_reason": ""
            }

    Return start_station, start_pta, start_ata, start_arrival_delay, start_ptd, start_atd, start_dept_delay. (distance from init will be seperate) 
    """
    if cancelled == False:
        start_station = location["location"]
        start_pta = location["gbtt_pta"]
        start_ata = location["actual_ta"]
        start_arrival_delay = get_delay(start_pta, start_ata)
        start_ptd = location["gbtt_ptd"]
        start_atd = location["actual_td"]
        start_dept_delay = get_delay(start_ptd, start_atd)
        return start_station, start_pta, start_ata, start_arrival_delay, start_ptd, start_atd, start_dept_delay
    else:
        start_station = location["location"]
        start_pta = location["gbtt_pta"]
        start_ata = None 
        start_arrival_delay = None 
        start_ptd = location["gbtt_ptd"]
        start_atd = None 
        start_dept_delay = None
        return start_station, start_pta, start_ata, start_arrival_delay, start_ptd, start_atd, start_dept_delay

def end_punc_details(location : dict, cancelled = False) -> Tuple:
    """
    Given a dictionary of the following form:
            {
                "location": "BWK",
                "gbtt_ptd": "1346",
                "gbtt_pta": "1345",
                "actual_td": "1346",
                "actual_ta": "1344",
                "late_canc_reason": ""
            }

    Return end_station, end_pta, end_ata, end_delay, delayed
    """

    if cancelled == False:
        end_station = location["location"]
        end_pta = location["gbtt_pta"]
        end_ata = location["actual_ta"]
        end_delay = get_delay(end_pta, end_ata) 
        if end_delay > 0:
            delayed = True
        else:
            delayed = False

        return end_station, end_pta, end_ata, end_delay, delayed
    else:
        end_station = location["location"]
        end_pta = location["gbtt_pta"]
        end_ata = None 
        end_delay = None
        delayed = None
        return end_station, end_pta, end_ata, end_delay, delayed

def is_cancelled(start_location: dict, end_location: dict) -> bool:
    if start_location["actual_td"] == "" or end_location["actual_ta"] == "":
        return True    
    else:
        return False

def late_canc_reason(start_location: dict, end_location: dict, cancelled=False) -> bool | None:
    if cancelled == False:
        if end_location["late_canc_reason"] == "":
            return None
        else:
            return end_location["late_canc_reason"]
    else:
        if start_location["actual_td"] == "":
            return start_location["late_canc_reason"]
        else:
            return end_location["late_canc_reason"]



def distance_between_stations(init_station: str, start_station : str) -> int | None:
    # Need to know all possible start stations.
    if init_station == "NCL" and start_station == "DAR":
        return 50 
    elif init_station == "EDB" and start_station == "DAR":
        return 190
    elif init_station == "GLC" and start_station == "DAR":
        return 228
    elif init_station == "ABD" and start_station == "DAR":
        return 293
    else:
        print(f"Initial Station {init_station} hasn't been hardcoded!")
        return None

"""

    Utilities for testing:

"""



if __name__ == '__main__':
    print(get_api_key())
