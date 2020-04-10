#!/usr/bin/env python
"""Scrapes the Robert-Koch-Institute website for covid-19 infections grouped by federal state"""
import requests
from bs4 import BeautifulSoup


def main():
    """The data is currently (march 15, 2020) updated on a daily basis, at 8pm"""
    url = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all("tr")
    for result in results[2:]:
        state = result.find("td").text
        confirmed = result.td.next_sibling.text.replace(".", "")
        deaths = result.findChildren("td")[4].text
        print(f"{state}: {confirmed}, deaths: {deaths}")


if __name__ == "__main__":
    main()
