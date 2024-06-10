# Leveraging g4g tutorial (src: https://www.geeksforgeeks.org/python-web-scraping-tutorial/)
import requests
from bs4 import BeautifulSoup

# Returns a Response object if get request is successful
def test_request(url):
    req = requests.get(url)
    if req:
        print('Stage 1: Request Succeed.')
        return req
    else:
        print('Stage 1: Request Failed.')
        return None
    
# Parses a Response object and returns data (MUST EDIT)
def parse_request(resp):
    # Parse HTML
    soup = BeautifulSoup(resp.content, 'html.parser')

    ''' ******** MODIFY SCRAPER FILTERS. ALL VARIABLES WITH '_' PREFIX SHOULD BE ADJUSTED******** '''
    # Find data table
    _course_tables = soup.find_all('table', {'class': 'table_default'})
    
    data = []
    # Iterate through multiple potential tables
    for table in _course_tables:
        _rows = table.find_all('tr')
        # Iterate and store data in array
        for row in _rows:
            _td = row.find('td', class_='width')
            if _td:
                _link = _td.find('a')
                if _link:
                    title = _link.get_text(strip=True)
                    title = title.replace("\xa0", " ")
                    data.append(title)

    if len(data) > 0:
        print('Stage 2: Parse Successful.')
        return data
    else: 
        print('Stage 2: Parse Failed? No Data.')
        return None

# Write data to specified output file
def write_data(data, output_path):
    with open(f'{output_path}.txt', 'w') as file:
        for item in data:
            file.write(item + '\n')
    print('Stage 3: Data Written.')

def main():
    ''' ******** ADD URL AND OUTPUT FILE PATH HERE ******** '''
    data = []
    for i in range(1, 39):
        print(f'Page Number: {i}')
        url = f'https://catalogs.buffalo.edu/content.php?catoid=1&catoid=1&navoid=18&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D={i}#acalog_template_course_filter'
        req = test_request(url)
        if req:
            data += parse_request(req)
    if data:
        file_path = 'test/test_outputs/ub_courses'
        write_data(data, file_path)
    else:
        print('Stage 3: Write Failed. No Data.')

if __name__ == '__main__':
    main()