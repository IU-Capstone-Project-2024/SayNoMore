import requests
from bs4 import BeautifulSoup
import csv


def write_to_csv(table):
    # Find all city links
    city_links = table.find_all('a', href=True)

    # Extract city names and codes
    city_data = []
    for link in city_links:
        href = link['href']
        if 'iata-country.php' in href:
            city_code = href.split('=')[-1]
            city_name = link.get_text()
            city_data.append((city_name, city_code))

    # Save the results to a CSV file
    csv_file = 'data/country_codes.csv'
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['City', 'Code'])  # Write the header
        writer.writerows(city_data)  # Write the data rows

    print(f'Data has been written to {csv_file}')

# URL to fetch the data from
url = "http://www.betravel.ru/iata-country-list.php"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all tables in the HTML
    tables = soup.find_all('table')

    # Loop through all tables and print them
    counter = 1
    for table in tables:
        if counter != 7:
            counter += 1
            continue
        write_to_csv(table)
        break
else:
    print("Failed to retrieve data. Status code:", response.status_code)
