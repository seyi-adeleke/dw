import xlrd
from urllib.parse import urljoin
from utils import url_is_valid, make_request, parse_sheet, write_csv, get_filename, convert_to_soup

url_dict = {
    "day": "https://www.eia.gov/dnav/ng/hist/rngwhhdD.htm",
    "month": "https://www.eia.gov/dnav/ng/hist/rngwhhdM.htm"
    }

xl_sheet_name = 'Data 1'

def main():
    for key in url_dict:
        url = url_dict[key]
        if (url_is_valid(url_dict[key])):
            html_data = make_request(url)
            soup_data = convert_to_soup(html_data)

            link_to_xls_file = soup_data.select_one("[href*='hist_xls']")
            xl_data = make_request(urljoin(url, link_to_xls_file["href"]))
            xl_workbook = xlrd.open_workbook(file_contents=xl_data.content)
            xl_sheet = xl_workbook.sheet_by_name(xl_sheet_name)

            parsed_data = parse_sheet(xl_sheet)
            filename = get_filename(key)

            write_csv(parsed_data, filename)
            print("Created CSV File: " + filename)
        else:
            print("Url Passed is not valid")

if __name__ == "__main__":
    main()
