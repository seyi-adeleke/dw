import requests
import csv
import xlrd

from urllib.parse import urlparse
from bs4 import BeautifulSoup

def url_is_valid(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def make_request(url):
    response = requests.get(url)
    return response

def convert_to_soup(data):
    return BeautifulSoup(data.content, features="html.parser")

def parse_sheet(xl_sheet):
    data = []
    for row in xl_sheet.get_rows():
        if(row[0].ctype == 3):
            price = row[1].value
            date = xlrd.xldate_as_datetime(row[0].value, 0).date().isoformat()
            data.append([date, price])
    return data

def write_csv(data, filename):
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Price'])
        writer.writerows(data)

def get_filename(key):
    filename = 'daily_gas_data.csv'
    if (key == 'month'):
        filename = "monthly_gas_data.csv"
        return filename
    else:
        return filename
