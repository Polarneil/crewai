import os
import requests
from langchain_community.tools import tool
from dotenv import load_dotenv

load_dotenv()


@tool("Weather API")
def retrieve_weather_data(latitude: str, longitude: str):
    """ Useful for retrieving weater data from an api given latitude and longitude """
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={os.getenv('OPENWEATHER_API_KEY')}"

    response = requests.get(url)

    return response.json()
