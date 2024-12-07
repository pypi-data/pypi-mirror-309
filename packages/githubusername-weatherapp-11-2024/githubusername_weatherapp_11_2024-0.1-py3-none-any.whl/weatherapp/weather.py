import requests
import time
from datetime import datetime

class Weather:
    def __init__(self):
        self.api_base_url = "https://api.open-meteo.com/v1/forecast"

    def display_current_weather(self, city, refresh_delay=10):
        """Affiche en temps réel les données météo actuelles pour une ville donnée."""
        while True:
            # Configurer les paramètres de requête
            params = {
                "latitude": city["latitude"],
                "longitude": city["longitude"],
                "current_weather": True,
            }
            
            # Envoyer la requête API
            response = requests.get(self.api_base_url, params=params)
            data = response.json()

            # Extraire les données météo
            weather = data.get("current_weather", {})
            temperature = weather.get("temperature")
            wind_speed = weather.get("windspeed")
            humidity = weather.get("relative_humidity")

            # Afficher les données dans le terminal
            print("\033c", end="")  # Clear terminal
            print(f"Météo actuelle pour {city['name']} :")
            print(f"Température : {temperature}°C")
            print(f"Vitesse du vent : {wind_speed} km/h")
            print(f"Humidité : {humidity}%")

            time.sleep(refresh_delay)

    def display_past_weather(self, city, time_start, time_end):
        """Affiche les données météo passées pour une ville donnée sur une période de temps."""
        # Vérifications
        now = datetime.now()
        if time_start >= now or time_end >= now:
            print("Les dates de début et de fin doivent être dans le passé.")
            return
        if time_end <= time_start:
            print("La date de fin doit être postérieure à la date de début.")
            return

        # Configurer les paramètres de requête pour l'historique météo
        params = {
            "latitude": city["latitude"],
            "longitude": city["longitude"],
            "start": time_start.isoformat(),
            "end": time_end.isoformat(),
            "hourly": "temperature_2m,wind_speed_10m,humidity_2m"
        }

        # Envoyer la requête API
        response = requests.get(self.api_base_url, params=params)
        data = response.json()

        # Extraire et afficher les données heure par heure
        temperatures = data["hourly"]["temperature_2m"]
        wind_speeds = data["hourly"]["wind_speed_10m"]
        humidities = data["hourly"]["humidity_2m"]
        
        print(f"Météo passée pour {city['name']} de {time_start} à {time_end} :")
        for i in range(len(temperatures)):
            print(f"Heure {i+1}: Température {temperatures[i]}°C, Vent {wind_speeds[i]} km/h, Humidité {humidities[i]}%")
