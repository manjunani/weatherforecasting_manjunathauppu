
#This code will fetch the weather details for the given city name.
#It will make use of geopy module to get the location details.
#It will make use of weatherapi.com to get the current weather details of the city.

from geopy.geocoders import Nominatim
from constants import *
import requests
import streamlit as st
import pandas as pd

url = "https://weatherapi-com.p.rapidapi.com/current.json"
headers = {
	"X-RapidAPI-Key": f"{API_KEY}",
	"X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}

def get_location_lat_lon(city_name):
    '''
    This function will return the latitude and longitude of the given city name.
    '''
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(f"{city_name}")
    if location != None:
        return location.latitude, location.longitude
    else:
        st.warning("Error Occured: Please Enter the City Name Again")
        st.stop()  

def get_weather_data(url, headers, lat, lon):
    '''
    This function will return the weather details of the given latitude and longitude.
    '''
    querystring = {"q": f"{lat},{lon}"}
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error Occured: Please try Again")
        st.stop()

def get_location_details(location):
    '''
    This function will return the location details of the given latitude and longitude.
    '''
    location_data = ''
    for k, v in location.items():
        if "epoch" in k:
            continue
        elif k in CHANGABLE_KEY_ITEMS and type(CHANGABLE_KEY_ITEMS[k]) == list:
            st.write(f"{CHANGABLE_KEY_ITEMS[k][0].title()}: {v} {CHANGABLE_KEY_ITEMS[k][1]}")
            location_data += f"{CHANGABLE_KEY_ITEMS[k][0]} is {v} {CHANGABLE_KEY_ITEMS[k][1]} and "
        elif k in CHANGABLE_KEY_ITEMS and type(CHANGABLE_KEY_ITEMS[k]) == str:
            st.write(f"{CHANGABLE_KEY_ITEMS[k].title()}: {v}")
            location_data += f"{CHANGABLE_KEY_ITEMS[k]} is {v} and "
        else:
            st.write(f"{k.capitalize()}: {v}")
            location_data += f"{k} is {v} and "
    st.title("Location Summary")
    st.write(location_data[:-5])

def get_current_weather_details(current):
    '''
    This function will return the current weather details of the given latitude and longitude.
    '''
    current_data = ''
    for k, v in current.items():
        if "epoch" in k or type(v) == dict:
            continue
        elif k in CHANGABLE_KEY_ITEMS and type(CHANGABLE_KEY_ITEMS[k]) == list:
            st.write(f"{CHANGABLE_KEY_ITEMS[k][0].title()}: {v} {CHANGABLE_KEY_ITEMS[k][1]}")
            current_data += f"{CHANGABLE_KEY_ITEMS[k][0]} is {v} {CHANGABLE_KEY_ITEMS[k][1]} and "
        elif k in CHANGABLE_KEY_ITEMS and type(CHANGABLE_KEY_ITEMS[k]) == str:
            st.write(f"{CHANGABLE_KEY_ITEMS[k].title()}: {v}")
            current_data += f"{CHANGABLE_KEY_ITEMS[k]} is {v} and "
        else:
            st.write(f"{k.capitalize()}: {v}")
            current_data += f"{k} is {v} and "
    st.title("Current Weather Summary")
    st.write(current_data[:-5])

if __name__ == "__main__":
    st.title("Weather Forecast App")
    city_name = st.text_input("Please Enter the City Name:",key=1)
    state = st.button("Go!..")
    if state:
        lat,lon = get_location_lat_lon(city_name)
        st.write("Hey There! You have entered the city name as: ", city_name)
        st.write("Fetching the Weather Details for the City: ", city_name)
        my_weather_data = get_weather_data(url, headers, lat, lon)
        st.map(pd.DataFrame(my_weather_data["location"],index=[0]))
        st.image(f'https:{my_weather_data["current"]["condition"]["icon"]}',caption=f"Current Weather in {city_name.capitalize()} is {my_weather_data['current']['condition']['text']}")
        st.title("Location Details")
        get_location_details(my_weather_data["location"])
        st.json(my_weather_data["location"])
        st.title("Current Weather Details")
        get_current_weather_details(my_weather_data["current"])
        st.json(my_weather_data["current"])
