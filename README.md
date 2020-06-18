# Captain Planet

## About

## covid-19

![covid-19](docs/clusters.png)

### report

Following the development of the pandemic with some visualizations and number crunching.

You can find the newest version of the report as [PDF here](covid-19/report.pdf).

### get data for germany

Get current covid-19 numbers for germany, detailed for each state:

`docker run --rm oembot/captain-planet covid-19/germany.py`

This is currently only returning some awkwardly formatted text and will be changed to json output soon.

Get current covid-19 numbers for hamburg, germany:

`docker run --rm oembot/captain-planet covid-19/hamburg.py`

This will return the numbers in json.
