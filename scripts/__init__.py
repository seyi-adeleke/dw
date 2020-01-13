import requests
import xlrd
import csv
from urllib.parse import urljoin
from utils import url_is_valid, make_request, parse_sheet, write_csv, get_filename

url_dict = {
    "day": "https://www.eia.gov/dnav/ng/hist/rngwhhdD.htm",
    "month": "https://www.eia.gov/dnav/ng/hist/rngwhhdM.htm"
    }

def main():
    for key in url_dict:
        url = url_dict[key]
        if (url_is_valid(url_dict[key])):
            soup_data = make_request(url)
            link_to_xls_file = soup_data.select_one("[href*='hist_xls']")
            xls_response = requests.get(urljoin(url, link_to_xls_file["href"]))
            workbook = xlrd.open_workbook(file_contents=xls_response.content)
            xl_sheet = workbook.sheet_by_name("Data 1")
            parsed_data = parse_sheet(xl_sheet)
            filename = parse_filename(key)
            write_csv(parsed_data, filename)
        else:
            print("Url Passed is not valid")

if __name__ == "__main__":
    main()
