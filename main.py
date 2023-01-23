import requests
from twilio.rest import Client


OWM_Endpoint = "https://api.openweathermap.org/data/3.0/onecall"
api_key = "your_OWM_api_key"
account_sid = "your_twilio/etc_account_sid"
auth_token = "your_auth_token"

phone_numbers = [
    {'number': '+19492784738', 'latitude': 40.7029667, 'longitude': -74.00733305555555},
    {'number': '+19092300452', 'latitude': 33.661949, 'longitude': -117.831383},
    {'number': '+19493958385', 'latitude': 33.584520, 'longitude': -117.644780}
]
for phone_number in phone_numbers:
    weather_params = {
        "lat": phone_number['latitude'],
        "lon": phone_number['longitude'],
        "appid": api_key,
        "exclude": "current,minutely,daily"

    }

    response = requests.get(OWM_Endpoint, params=weather_params)
    response.raise_for_status()
    weather_data = response.json()

    will_rain = False

    weather_slice = weather_data["hourly"][:12]
    for hour_data in weather_slice:
        condition_code = (hour_data["weather"][0]["id"])
        if int(condition_code) < 700:
            will_rain = True
    if will_rain:
        client = Client(account_sid, auth_token)
        numbers_list = ["+19492784738", "+19092300452", "19493958385"]
        message = client.messages \
            .create(
            body=f"It's going to rain today, bring an umbrella bro!{chr(0x2614)}{chr(0x1F62E)}",
            from_='+12029295371',
            to=phone_number['number']
        )
        print(message.status)
