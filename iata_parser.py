import requests
from bs4 import BeautifulSoup
import csv

# Base URL of the website, adjust if necessary
base_url = 'https://www.nationsonline.org/oneworld/IATA_Codes/airport_code_'  # Replace with the actual base URL

# List of alphabets to iterate over, with 'xyz' included
alphabets = list('abcdefghijklmnopqrstuvw')
alphabets.append('xyz')

# Initialize a list to hold the parsed data
parsed_data = []

# Iterate over each alphabet page
for letter in alphabets:
    # Construct the URL for the current letter
    url = f'{base_url}{letter}.htm'
    
    # Fetch the HTML content of the webpage
    response = requests.get(url)
    webpage = response.content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(webpage, 'html.parser')

    # Find the table containing the data
    table = soup.find('table')

    # Check if the table exists on the page
    if not table:
        print(f"No table found on page for {letter}")
        continue

    # Loop through the rows of the table
    for row in table.find_all('tr')[1:]:  # Skipping the header row
        cols = row.find_all('td')
        if len(cols) >= 4:
            city = cols[0].text.strip()
            airport = cols[1].text.strip()
            country = cols[2].text.strip()
            iata_code = cols[3].text.strip()
            
            # Append the parsed data to the list
            parsed_data.append([city, airport, country, iata_code])

# Write the parsed data to a CSV file
csv_file_path = 'airport_codes.csv'
with open(csv_file_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['City', 'Airport/Location', 'Country', 'IATA Code'])
    writer.writerows(parsed_data)

print(f"Data has been successfully written to {csv_file_path}")