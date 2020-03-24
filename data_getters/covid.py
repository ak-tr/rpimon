# This script runs every 6 minutes of the hour from a corn schedule
# The main display.py program updates to catch this data every 5 minutes

from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import tempfile

temp_dir = tempfile.gettempdir()
file_path = temp_dir + "/coviddata.txt"

def get_covid_stats():
    url = "https://www.worldometers.info/coronavirus/country/uk/"
    url2 = "https://www.worldometers.info/coronavirus/"

    # Get response from first URL which contains data about UK cases and deaths
    response = requests.get(url)

    # Get response from second URL which contains worldwide cases and deaths
    response2 = requests.get(url2)

    # Use BeautifulSoup library to parse the URLs we just retrieved
    soup = BeautifulSoup(response.text, "html.parser")
    soup2 = BeautifulSoup(response2.text, "html.parser")

    # Create empty array called stats
    stats = []

    # For each statement to catch all lines of code that contain h1 tag
    for el in soup.findAll('h1'):
        if "Coronavirus" in str(el):
            stats.append((re.sub('<[^<]+?>', '', str(el.find_next_sibling())).replace(" ", "").replace("\n", "")))
        elif "Deaths" in str(el):
            stats.append((re.sub('<[^<]+?>', '', str(el.find_next_sibling())).replace(" ", "").replace("\n", "")))
        elif "Recovered" in str(el):
            stats.append((re.sub('<[^<]+?>', '', str(el.find_next_sibling())).replace(" ", "").replace("\n", "")))

    for el in soup2.findAll('h1'):
        if "Coronavirus" in str(el):
            stats.append((re.sub('<[^<]+?>', '', str(el.find_next_sibling())).replace(" ", "").replace("\n", "")))
        elif "Deaths" in str(el):
            stats.append((re.sub('<[^<]+?>', '', str(el.find_next_sibling())).replace(" ", "").replace("\n", "")))
        elif "Recovered" in str(el):
            stats.append((re.sub('<[^<]+?>', '', str(el.find_next_sibling())).replace(" ", "").replace("\n", "")))

    stats.append(datetime.now().strftime("%d %b, %Y %H:%M:%S"))

    return stats

stats = get_covid_stats()

with open(file_path, 'w') as file:
    for el in stats:
        file.writelines(str(el) + "\n")
