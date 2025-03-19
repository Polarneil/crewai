from crewai import Agent
from textwrap import dedent
from WeaterAPI import retrieve_weather_data
from crewai import LLM
from dotenv import load_dotenv
import os

load_dotenv()


class WeatherAgents:
    def __init__(self):
        self.OpenAIGPT35 = LLM(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        self.OpenAIGPT4o = LLM(
            model="gpt-4o",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        self.Gemini2Flash = LLM(
            model='gemini/gemini-2.0-flash',
            api_key=os.getenv("GEMINI_API_KEY"),
        )
        self.Ollama = LLM(
            model="ollama/llama3.1:8b",
            base_url="http://localhost:11434",
        )
        self.CrederaProxy = LLM(
            model="gpt-4o",
            base_url="http://0.0.0.0:4000",
            api_key="sk-mnu6FpF-NrGmNY2E8L8OcQ"
        )

    def weather_agent(self):
        return Agent(
            role="Weather Data Retriever",
            backstory=dedent(f"""You are a renowned Weather Data Retriever."""),
            goal=dedent(f"""
            Convert geolocations to longitude and latitude coordinates.
            Retrieve weather data from the Weather API endpoint.
            """),
            tools=[retrieve_weather_data],
            allow_delegation=False,
            verbose=True,
            llm=self.CrederaProxy,
        )

    def writer_agent(self):
        return Agent(
            role="Weather Analyst",
            backstory=dedent(f"""You have spent your entire life reporting on weather data."""),
            goal=dedent(f"""Take the information from the weather agent and present a report to the general public."""),
            allow_delegation=False,
            verbose=True,
            llm=self.CrederaProxy,
        )
