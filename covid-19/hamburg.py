#!/usr/bin/env python
"""Scrapes hamburg.de/corona-zahlen for detailed covid-19 numbers for hamburg."""

import json
import re
import requests
from bs4 import BeautifulSoup


def crawl_covid19_stats():
    """Crawls hamburg.de for detailed covid-19 numbers and returns them as a dict"""
    url = "https://www.hamburg.de/corona-zahlen/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    infections = _parse_infections(soup)
    deaths = _parse_deaths(soup)
    hospitalizations = _parse_hospitalizations(soup)
    boroughs = _parse_boroughs(soup)
    trend = _parse_trend(soup)
    return {**infections, **deaths, **hospitalizations, **boroughs, **trend}


def _parse_infections(soup):
    return _parse_body(
        soup,
        ["confirmed-total", "recovered", "new infections"],
        ".c_chart.one .chart_legend li",
    )


def _parse_deaths(soup):
    return _parse_body(
        soup, ["deaths-total", "new deaths"], ".c_chart.two .chart_legend li"
    )


def _parse_hospitalizations(soup):
    return _parse_body(
        soup,
        ["hospitalizations-total", "intensive-care", "intensive-care-from-hamburg"],
        ".c_chart.three .chart_legend li",
    )


def _parse_body(soup, labels, selector):
    tags = soup.select(selector)
    tags = [re.search(r"\d+$", tag.text) for tag in tags]
    tags = [int(tag.group(0)) for tag in tags if tag]
    return dict(zip(labels, tags))


def _parse_boroughs(soup):
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


def _parse_trend(soup):
    tags = soup.select(".cv_chart_container .value_show")
    tags = [int(tag.text) for tag in tags]
    return {"new_confirmed_in_last_seven_days": tags}


if __name__ == "__main__":
    print(json.dumps(crawl_covid19_stats()))
