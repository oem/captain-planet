import requests
import wget

if __name__ == "__main__":
    page = requests.get(
        "https://ourworldindata.org/co2-and-other-greenhouse-gas-emissions"
    )
