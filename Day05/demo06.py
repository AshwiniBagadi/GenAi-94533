# Input city name from user.
# Get current weather from weather API.
# Ask LLM to explain the weather in English.

import os
import requests
from langchain.chat_models import init_chat_model

from dotenv import load_dotenv

load_dotenv()

llm = init_chat_model(
    model = "llama-3.3-70b-versatile",
    model_provider = "openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key = os.getenv("groq_api")
)
conversation = [
    {"role": "system", "content": "You are weather expert. but explains in short and only main details."}
]

while True:
    city= input("City name: ")
    if city=="exit":
        break
    api=os.getenv("weather_api")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&units=metric"
    response=requests.get(url)
    weather=response.json()
    info=print(weather['main']['temp'])

    
    llm_input=f"""
        Input: City name string
        live weather: {info} indicates temperature and {weather} has some details like humidity and etc.
        Question: get current weather and explain weather for the city.

        Instructions:
            give details for the weather in the given city in short. 
            give a short on the point explaination is 3-4 short points.

    """
    result=llm.invoke(llm_input)
    print(result.content)

