#!/usr/bin/env python
"""Scrapes hamburg.de/corona-zahlen for detailed covid-19 numbers for hamburg."""

import json
import re
import requests
from bs4 import BeautifulSoup


def parse_infections(soup):
    return parse_body(
        soup,
        ["confirmed-total", "recovered", "new infections"],
        ".c_chart.one .chart_legend li",
    )


def parse_deaths(soup):
    return parse_body(
        soup, ["deaths-total", "new deaths"], ".c_chart.two .chart_legend li"
    )


def parse_hospitalizations(soup):
    return parse_body(
        soup,
        ["hospitalizations-total", "intensive-care", "intensive-care-from-hamburg"],
        ".c_chart.three .chart_legend li",
    )


def parse_body(soup, labels, selector):
    """parse selected content from the crawled webpage and label it"""
    tags = soup.select(selector)
    tags = [re.search(r"\d+$", tag.text) for tag in tags]
    tags = [int(tag.group(0)) for tag in tags if tag]
    return dict(zip(labels, tags))


def main():
    """The data is being updated on a daily basis"""
    url = "https://www.hamburg.de/corona-zahlen/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    infections = parse_infections(soup)
    deaths = parse_deaths(soup)
    hospitalizations = parse_hospitalizations(soup)
    print(json.dumps({**infections, **deaths, **hospitalizations}))


if __name__ == "__main__":
    main()
