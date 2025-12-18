import streamlit as st
import os
import requests
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

st.title("WEATHER APP")

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("groq_api")
)

conversation = [
    {
        "role": "system",
        "content": "You are a weather expert. Explain the weather briefly using only main details."
    }
]

city = st.chat_input("City name..")

if city:
    api = os.getenv("weather_api")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&units=metric"
    response = requests.get(url)
    weather = response.json()

    if response.status_code != 200:
        st.error("Invalid city name or API issue.")
    else:
        temp = weather["main"]["temp"]
        humidity = weather["main"]["humidity"]
        description = weather["weather"][0]["description"]

        llm_input = f"""
        City: {city}
        Temperature: {temp}°C
        Humidity: {humidity}%
        Condition: {description}

        Explain the current weather in 3–4 short bullet points.
        """

        result = llm.invoke(llm_input)
        st.write(result.content)
