import concurrent.futures
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import threading

progress = 0
step = 0

def write_to_csv(table, lock):
    # Find all city links
    city_links = table.find_all('a', href=True)

    # Extract city names and codes
    city_data = []
    for link in city_links:
        href = link['href']
        if 'iata-city-code.php' in href:
            city_code = href.split('=')[-1]
            city_name = link.get_text()
            city_data.append((city_name, city_code))

    # Save the results to a CSV file
    csv_file = '../../data/all_cities_codes.csv'

    with lock:
        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['city', 'Code'])  # Write the header
            writer.writerows(city_data)  # Write the data rows

    # print(f'Data has been written to {csv_file}')


def request_country(country, lock):
    global progress
    for letter in range(192, 224):
        url = f"http://www.betravel.ru/iata-city-alphabet.php?country={country}&alphabet=%{format(letter, 'x')}"
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all tables in the HTML
            tables = soup.find_all('table')

            write_to_csv(tables[6], lock)
        else:
            print("Failed to retrieve data. Status code:", response.status_code)
    progress += step
    print(f'Progress = {progress:.2f}%')


if __name__ == "__main__":
    df = pd.read_csv('../../data/country_codes.csv')
    countries = df['Code']
    lock = threading.Lock()
    step = 1/len(countries)*100
    with concurrent.futures.ThreadPoolExecutor(10) as executor:
        executor.map(lambda country: request_country(country, lock), countries)