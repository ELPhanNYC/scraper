# Leveraging g4g tutorial (src: https://www.geeksforgeeks.org/python-web-scraping-tutorial/)
import requests
from bs4 import BeautifulSoup

# returns a Response object if get request is successful
def test_request(url):
    req = requests.get(url)
    if req:
        print('Stage 1: Request Succeed.')
        return req
    else:
        print('Stage 1: Request Failed.')
        return None
    
# Parses a Response object (**Must be modified)
def parse_request(resp):
    # Parse HTML
    soup = BeautifulSoup(resp.content, 'html.parser')

    # Find data table
    course_table = soup.find('table', {'class': 'table_default'})
    
    # Get all 'tr' elements (table rows)
    rows = course_table.find_all('tr')

    data = []
    # Iterate and store data in array
    for row in rows:
        td = row.find('td', class_='width')
        if td:
            link = td.find('a')
            if link:
                title = link.get_text(strip=True)
                title = title.replace("\xa0", " ")
                data.append(title)
    if len(data) > 0:
        print('Stage 2: Parse Successful.')
        return data
    else: 
        print('Stage 2: Parse Failed? No Data.')
        return None

def write_data(data, output_path):
    with open(f'{output_path}.txt', 'w') as file:
        for item in data:
            file.write(item + '\n')
    print('Stage 3: Data Written.')

def main():
    url = 'https://catalogs.buffalo.edu/content.php?filter%5B27%5D=CSE&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=1&expand=&navoid=18&search_database=Filter#acalog_template_course_filter'
    file_path = 'test/test_outputs/cse_course_ub'
    
    req = test_request(url)
    if req:
        data = parse_request(req)
        if data:
            write_data(data, file_path)
        else:
            print('Stage 3: Write Failed. No Data.')

if __name__ == '__main__':
    main()