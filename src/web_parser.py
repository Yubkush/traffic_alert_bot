"""Module to parse for soccer games"""

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

r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html.parser')

paragraphs = [p.string for p in soup.find_all('p')]

for p in paragraphs:
    strs = p.split()
    if len(strs) == 3 and is_date(strs[1]):
        date = datetime.strptime(strs[1], '%d/%m/%Y').date()
        date_str = strs[1]
        time_str = strs[2]
        print(f"There is a game on {get_week_day_str(date)} the {strs[1]} at {strs[2]}")
