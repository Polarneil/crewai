import requests
from langchain_community.tools import tool


@tool("Weather API")
def retrieve_weather_data(latitude: str, longitude: str):
    """ Useful for retrieving weater data from an api given latitude and longitude """
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid=7f2cf6040f9e28721de531468d34985e"

    response = requests.get(url)

    return response.json()
