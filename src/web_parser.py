from datetime import datetime
import requests
from bs4 import BeautifulSoup

URL = "https://www.haifa-stadium.co.il/%d7%9c%d7%95%d7%97_%d7%94%d7%9e%d7%a9%d7%97%d7%a7%d7%99%d7%9d_%d7%91%d7%90%d7%a6%d7%98%d7%93%d7%99%d7%95%d7%9f/"
WEEKDAYS = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'
]

def get_week_day_str(date_str: datetime.date):
    return WEEKDAYS[date_str.weekday()]

def is_date(date_string: str):
    try:
        datetime.strptime(date_string, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def is_game_info(strs: list[str]):
    return len(strs) == 3

def get_week_game_data() -> str:
    try:
        r = requests.get(URL)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        r = None

    if r:
        parser = BeautifulSoup(r.content, 'html.parser')

        paragraphs = [p.string for p in parser.find_all('p')]

        res = ""
        for p in paragraphs:
            details = p.split()
            if is_game_info(details) and is_date(details[1]):
                date = datetime.strptime(details[1], '%d/%m/%Y').date()
                [_, date_str, time_str] = details
                res += f"There is a game on {get_week_day_str(date)} the {date_str} at {time_str}\n"

        return res
    
    return ""

if __name__ == "__main__":
    get_week_game_data()
