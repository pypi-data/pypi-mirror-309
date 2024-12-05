from prog5lr33.prog5lr33.owm_key import owm_api_key
import json
import prog5lr33.prog5lr33.getweatherdata_test as wetest

def get_weather_data(place, api_key=None):


    import requests
       
    response = requests.get(
        f'https://ru.api.openweathermap.org/data/2.5/weather?q={place}&appid={api_key}') 
    response.encoding = 'utf-8'
    res_object = response.text

    return res_object
  
if __name__ == "__main__":
    pass
    print(get_weather_data('Moscow',api_key=owm_api_key))
    print(get_weather_data('Saint Petersburg',api_key=owm_api_key))
    print(get_weather_data('Dhaka',api_key=owm_api_key))

