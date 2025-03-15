from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

URL = "https://www.haifa-stadium.co.il/%d7%9c%d7%95%d7%97_%d7%94%d7%9e%d7%a9%d7%97%d7%a7%d7%99%d7%9d_%d7%91%d7%90%d7%a6%d7%98%d7%93%d7%99%d7%95%d7%9f/"
WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def get_week_day_str(date_str):
    return WEEKDAYS[date_str.weekday()]


def find_date_time(words: list[str]):
    date = None
    time = None
    for string in words:
        parts = string.split('/')
        if len(parts) == 3 and all(part.isdigit() for part in parts):
            [day, month, year] = parts
            # add "0" padding for day & month
            if len(day) == 1:
                day = "0" + day
            if len(month) == 1:
                month = "0" + month
            # add "20" if needed in year
            if len(year) == 2:
                year = "20" + year    
            date = f"{day}/{month}/{year}"
            continue
        
        parts = string.split(':')
        if len(parts) == 2 and all(part.isdigit() for part in parts):
            time = string
            continue
    
    return date, time


def is_game_tomorrow(date):
    return date == datetime.today().date() + timedelta(days=1)


def get_paragraphs() -> list[str]:
    try:
        r = requests.get(URL)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        r = None

    if r:
        parser = BeautifulSoup(r.content, "html.parser")

        paragraphs = [p.string for p in parser.find_all("p")]

        return paragraphs

    return []


def get_tomorrows_game_data() -> str:
    res = ""
    for p in get_paragraphs():
        details = p.split()
        (date, time) = find_date_time(details)
        if date is not None and time is not None:
            date_formatted = datetime.strptime(date, "%d/%m/%Y").date()
            if is_game_tomorrow(date_formatted):
                res += f"There is a game tomorrow {get_week_day_str(date_formatted)} the {date} at {time}\n"
    return res

if __name__ == "__main__":
    print(get_tomorrows_game_data())
