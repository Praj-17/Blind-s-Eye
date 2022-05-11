import requests

import geocoder
g = geocoder.ip('me')
api_key = "1acce5470dcf10cb9662c26b101f3c05"

# Python program to find current
# weather details of any city
# using openweathermap api
 
# import required modules
import requests, json
def weather_from_city(city_name): 
    # Enter your API key here
    
    # base_url variable to store url
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    

    # complete_url variable to store
    # complete url address
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    # get method of requests module
    # return response object
    try:
        response = requests.get(complete_url)
    
    # json method of response object
    # convert json format data into
    # python format data
        x = response.json()
    
    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found
        if x["cod"] != "404":
        
            # store the value of "main"
            # key in variable y
            y = x["main"]
        
            # store the value corresponding
            # to the "temp" key of y
            current_temperature = y["temp"]
        
            # store the value corresponding
            # to the "pressure" key of y
            current_pressure = y["pressure"]
        
            # store the value corresponding
            # to the "humidity" key of y
            current_humidity = y["humidity"]
        
            # store the value of "weather"
            # key in variable z
            z = x["weather"]
        
            # store the value corresponding
            # to the "description" key at
            # the 0th index of z
            weather_description = z[0]["description"]
        
            # print following values
            weather_dict ={ 'Temperature':str(current_temperature),
                            'Pressure':str(current_pressure),
                            'Humidity':str(current_humidity),
                            'Description':str(weather_description)} 
            return weather_dict
            
        else:
            return (" City Not Found ")
    except Exception as e:
        print("Exception: ", e)
def weather_local():
    api_url = "https://fcc-weather-api.glitch.me/api/current?lat=" + \
        str(g.latlng[0]) + "&lon=" + str(g.latlng[1])
    data = requests.get(api_url)
    data_json = data.json()
    if data_json['cod'] == 200:
        main = data_json['main']
        weather_desc = data_json['weather'][0]
        return [("weather of your current location is : "),
        ('weather type ' + weather_desc['main']),
        ('Temperature: ' + str(main['temp']) + 'degree celcius'), ]  
            
# Ladtitude Longititude , current location
def Location():
    api_url = "https://fcc-weather-api.glitch.me/api/current?lat=" + \
        str(g.latlng[0]) + "&lon=" + str(g.latlng[1])
    data = requests.get(api_url)
    data_json = data.json()
    if data_json['cod'] == 200:
        return [(str(data_json['coord']['lat']) + 'latitude' + str(data_json['coord']['lon']) + 'longitude')
        ('Current location is ' + data_json['name'] + data_json['sys']['country'] + 'dia')]

## humidity and wind speed
def weather_updates():  
    api_url = "https://fcc-weather-api.glitch.me/api/current?lat=" + \
        str(g.latlng[0]) + "&lon=" + str(g.latlng[1])

    data = requests.get(api_url)
    data_json = data.json()
    if data_json['cod'] == 200:
        main = data_json['main']
        wind = data_json['wind']
        return[('Wind speed is ' + str(wind['speed']) + ' metre per second')
        ('Humidity is ' + str(main['humidity']))]
        

                           

