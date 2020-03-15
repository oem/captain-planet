#!/usr/bin/env python
"""Scrapes the Robert-Koch-Institute website for covid-19 infections grouped by federal state"""
import re
import requests
from bs4 import BeautifulSoup


def main():
    """The data is currently (march 15, 2020) updated on a daily basis, at 8pm"""
    url = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all("tr")
    for result in results[1:-1]:
        state = result.find("td").text
        confirmed = result.td.next_sibling.text
        confirmed, deaths = parse_confirmed(confirmed)
        print(f"{state}: {confirmed}, deaths: {deaths}")


def parse_confirmed(confirmed):
    """Extracts death toll from total confirmed number."""
    confirmed = confirmed.replace(".", "")
    pattern = re.compile("^(.+?)\s*\((.+)\)$")
    match = re.search(pattern, confirmed)
    if match is None:
        return int(confirmed), 0
    return int(match.group(1)), int(match.group(2))


if __name__ == "__main__":
    main()
