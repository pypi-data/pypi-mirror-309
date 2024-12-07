import requests
import time
from datetime import datetime

class Weather:
    def __init__(self, api_url="https://api.open-meteo.com/v1/forecast"):
        self.api_url = api_url

    def display_current_weather(self, city_coordinates, refresh_delay):
        if refresh_delay < 1:
            raise ValueError("Le délai d'actualisation doit être supérieur ou égal à 1 seconde.")
        
        
        i=1
        while True:
            response = requests.get(
                self.api_url,
                params={
                    "latitude": city_coordinates[0],
                    "longitude": city_coordinates[1],
                    "current_weather": True,
                },
            )
            if response.status_code == 200:
                
               
                # i+=1
                # print("eeeee",i)
                # print (response.json())
                weather_data = response.json()["current_weather"]
                # print("eeeee")
                self.clear_terminal()
                formatted_data = {
                    "Température (°C)": weather_data["temperature"],
                    "Vent (km/h)": weather_data["windspeed"],
                    "Humidité (%)": weather_data["relativehumidity"]
                }
                print (weather_data)
                print("="*40)
                print(f"Température : {weather_data['temperature']}°C")
                print("="*40)
                print(f"Vitesse du vent : {weather_data['windspeed']} km/h")
                return formatted_data
            else:
                print("Erreur lors de la récupération des données météo.")
            time.sleep(refresh_delay)
    @staticmethod
    def clear_terminal():
        print("\033c", end="") 
        
    def display_past_weather(self, city_coordinates, time_start, time_end):
        if datetime.fromisoformat(time_start) >= datetime.now() or datetime.fromisoformat(time_end) >= datetime.now():
            raise ValueError("Les dates doivent être dans le passé.")
        if datetime.fromisoformat(time_start) >= datetime.fromisoformat(time_end):
            raise ValueError("time_end doit être postérieur à time_start.")
        
        response = requests.get(
            self.api_url,
            params={
                "latitude": city_coordinates[0],
                "longitude": city_coordinates[1],
                "start": time_start,
                "end": time_end,
                "hourly": "temperature_2m,windspeed_10m,relativehumidity_2m",
            },
        )
        if response.status_code == 200:
            # print("="*40)
            # print(response.json())
            print("="*40)   
            weather_data = response.json()["hourly"]   
            # print(weather_data)
            formatted_data = [
                {
                    "Temps": weather_data["time"][i],
                    "Température (°C)": weather_data["temperature_2m"][i],
                    "Vent (km/h)": weather_data["windspeed_10m"][i],
                    "Humidité (%)": weather_data["relativehumidity_2m"][i]
                }
                for i in range(len(weather_data["time"]))
            ]  
            print("Données météo passées :")
            for i, temp in enumerate(weather_data["temperature_2m"]):
                print(
                    f"Temps : {weather_data['time'][i]}, "
                    f"Température : {temp}°C, "
                    f"Vent : {weather_data['windspeed_10m'][i]} km/h, "
                    f"Humidité : {weather_data['relativehumidity_2m'][i]}%"
                )
            return formatted_data    
        else:
            print("Erreur lors de la récupération des données météo.")           
            

if __name__ == "__main__":
    weather = Weather()
    # weather.display_current_weather((48.8566, 2.3522), refresh_delay=5)
    weather.display_past_weather((48.8566, 2.3522), "2024-11-01T00:00", "2024-11-05T23:59")