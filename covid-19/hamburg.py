#!/usr/bin/env python
"""Scrapes hamburg.de/corona-zahlen for detailed covid-19 numbers for hamburg."""

import json
import re
import requests
from bs4 import BeautifulSoup


def parse_infections(soup):
    """Parses current infection numbers from the crawled webpage"""
    return parse_body(
        soup,
        ["confirmed-total", "recovered", "new infections"],
        ".c_chart.one .chart_legend li",
    )


def parse_deaths(soup):
    """Parses the current numbers for deaths due to covid-19 from the webpage"""
    return parse_body(
        soup, ["deaths-total", "new deaths"], ".c_chart.two .chart_legend li"
    )


def parse_hospitalizations(soup):
    """Parses the current numbers for hospitalizations from the webpage"""
    return parse_body(
        soup,
        ["hospitalizations-total", "intensive-care", "intensive-care-from-hamburg"],
        ".c_chart.three .chart_legend li",
    )


def parse_body(soup, labels, selector):
    """Parse selected content from the crawled webpage and label it"""
    tags = soup.select(selector)
    tags = [re.search(r"\d+$", tag.text) for tag in tags]
    tags = [int(tag.group(0)) for tag in tags if tag]
    return dict(zip(labels, tags))


def parse_boroughs(soup):
    """Parse borough data from webcrawler"""
    tags = soup.select(".table-article tr")[18:]
    tags = [tag.find_all("td") for tag in tags]
    tags = [
        {
            "name": tag[0].text,
            "confirmed": int(tag[1].text),
            "difference": int(tag[2].text.replace(" ", "")),
        }
        for tag in tags
    ]
    return {"boroughs": tags}


def parse_trend(soup):
    """Parses the seven-day chart"""
    tags = soup.select(".cv_chart_container .value_show")
    tags = [int(tag.text) for tag in tags]
    return {"new_confirmed_in_last_seven_days": tags}


def collect_stats():
    """Crawls hamburg.de for detailed covid-19 numbers"""
    url = "https://www.hamburg.de/corona-zahlen/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    infections = parse_infections(soup)
    deaths = parse_deaths(soup)
    hospitalizations = parse_hospitalizations(soup)
    boroughs = parse_boroughs(soup)
    trend = parse_trend(soup)
    return json.dumps({**infections, **deaths, **hospitalizations, **boroughs, **trend})


def main():
    """The data is being updated on a daily basis"""
    print(collect_stats())


if __name__ == "__main__":
    main()
