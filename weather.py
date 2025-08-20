import streamlit as st
import requests
import pandas as pd
import random

st.title("Weather Predictor 🌤️ (Interactive Playlists & Wallpapers)")

city = st.text_input("Enter city name:")

if st.button("Get Weather"):
    if city:
        # 1️⃣ Get latitude & longitude
        geo_url = f"https://nominatim.openstreetmap.org/search?format=json&q={city}"
        headers = {"User-Agent": "weather-app-example"}
        geo_response = requests.get(geo_url, headers=headers).json()

        if geo_response:
            lat = geo_response[0]["lat"]
            lon = geo_response[0]["lon"]

            # 2️⃣ Get weather data
            weather_url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lon}"
                f"&hourly=temperature_2m,relativehumidity_2m,weathercode&daily=temperature_2m_max,temperature_2m_min,weathercode&current_weather=true&timezone=auto"
            )
            weather_data = requests.get(weather_url).json()

            if "current_weather" in weather_data:
                cw = weather_data["current_weather"]

                # 3️⃣ Define playlists for each weather type
                playlists = {
                    "sunny": [
                        "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
                        "https://open.spotify.com/playlist/37i9dQZF1DX0UrRvztWcAU"
                    ],
                    "cloudy": [
                        "https://open.spotify.com/playlist/37i9dQZF1DX4E3UdUs7fUx",
                        "https://open.spotify.com/playlist/37i9dQZF1DX9uKNf5jGX6m"
                    ],
                    "foggy": [
                        "https://open.spotify.com/playlist/37i9dQZF1DWYcDQ1hSjOpY",
                        "https://open.spotify.com/playlist/37i9dQZF1DX3m3zKze42Fr"
                    ],
                    "rainy": [
                        "https://open.spotify.com/playlist/37i9dQZF1DXbvABJXBIyiY",
                        "https://open.spotify.com/playlist/37i9dQZF1DX1dxt3g7XnYl"
                    ],
                    "snowy": [
                        "https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6",
                        "https://open.spotify.com/playlist/37i9dQZF1DX4jSp2vNSw1t"
                    ],
                    "stormy": [
                        "https://open.spotify.com/playlist/37i9dQZF1DX0SM0LYsmbMT",
                        "https://open.spotify.com/playlist/37i9dQZF1DX5gV5x5lB9wM"
                    ],
                    "neutral": [
                        "https://open.spotify.com/playlist/37i9dQZF1DX4WgZiuR77Ef",
                        "https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0"
                    ]
                }

                # 4️⃣ Assign weather type based on code
                code = cw['weathercode']
                if code in [0,1]:
                    weather_type = "sunny"
                    bg_color = "#FFD700"
                    mood = "Sunny and cheerful! Perfect day for a walk ☀️"
                    recommendation = "Wear sunglasses and sunscreen."
                elif code in [2,3]:
                    weather_type = "cloudy"
                    bg_color = "#B0C4DE"
                    mood = "Partly cloudy. Calm day ahead 🌤️"
                    recommendation = "A light jacket might be comfortable."
                elif code in [45,48]:
                    weather_type = "foggy"
                    bg_color = "#A9A9A9"
                    mood = "Foggy weather, mysterious vibes 🌫️"
                    recommendation = "Drive carefully and avoid long walks."
                elif code in [51,53,55,56,57,61,63,65,66,67,80,81,82]:
                    weather_type = "rainy"
                    bg_color = "#87CEFA"
                    mood = "Rainy mood 🌧️"
                    recommendation = "Carry an umbrella and enjoy indoor activities."
                elif code in [71,73,75,77,85,86]:
                    weather_type = "snowy"
                    bg_color = "#E0FFFF"
                    mood = "Snowy wonderland ❄️"
                    recommendation = "Stay warm and enjoy hot drinks."
                elif code in [95,96,99]:
                    weather_type = "stormy"
                    bg_color = "#FFA500"
                    mood = "Thunderstorm alert! ⚡"
                    recommendation = "Stay indoors for safety."
                else:
                    weather_type = "neutral"
                    bg_color = "#FFFFFF"
                    mood = "Weather is unusual 🌈"
                    recommendation = "Check local conditions for safety."

                # 5️⃣ Randomly pick a playlist
                playlist_link = random.choice(playlists[weather_type])

                # 6️⃣ Apply background and display
                st.markdown(
                    f"<div style='background-color:{bg_color};padding:20px;border-radius:10px'>",
                    unsafe_allow_html=True
                )
                st.subheader(f"Current Weather in {city.title()}")
                st.write(f"Temperature: {cw['temperature']}°C")
                st.write(f"Windspeed: {cw['windspeed']} km/h")
                st.write(f"Weather code: {cw['weathercode']}")
                st.subheader("Weather Mood Predictor")
                st.write(mood)
                st.subheader("Weather-Based Recommendation")
                st.write(recommendation)
                st.subheader("Mood Playlist")
                st.markdown(f"[Click here to play a random playlist]({playlist_link})")
                st.markdown("</div>", unsafe_allow_html=True)

                # 7️⃣ Next 24 hours temperature & humidity
                st.subheader("Next 24 Hours Temperature & Humidity")
                temps = weather_data["hourly"]["temperature_2m"][:24]
                humidity = weather_data["hourly"]["relativehumidity_2m"][:24]
                df = pd.DataFrame({"Temperature (°C)": temps, "Humidity (%)": humidity})
                st.line_chart(df)

                # 8️⃣ 7-day forecast
                st.subheader("7-Day Forecast")
                daily = weather_data["daily"]
                df_daily = pd.DataFrame({
                    "Max Temp (°C)": daily["temperature_2m_max"],
                    "Min Temp (°C)": daily["temperature_2m_min"],
                    "Weather Code": daily["weathercode"]
                })
                st.dataframe(df_daily)

            else:
                st.error("Could not fetch weather data.")
        else:
            st.error("City not found.")
    else:
        st.warning("Please enter a city name.")
