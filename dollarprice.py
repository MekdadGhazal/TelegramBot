
import http.client
import json
import requests

def dollar():

    conn = http.client.HTTPSConnection("api.currencyfreaks.com")
    payload = ''
    headers = {}
    conn.request("GET", "https://api.currencyfreaks.com/v2.0/rates/latest?apikey=712082cb068b49129f14e8d3803cc5e9", payload, headers)
    res = conn.getresponse()
    data = res.read()

    parsed = json.loads(data)
    rates = parsed.get("rates", {})
    return {
        "SYP": rates.get("SYP"),
        "EUR": rates.get("EUR")
    }


print(dollar())



def price():
    # Where USD is the base currency you want to use
    url = "https://v6.exchangerate-api.com/v6/76b938a7b3b412f8c5bf5e50/latest/USD"

    # Making our request
    response = requests.get(url)
    data = response.json()

    rates = data.get("conversion_rates", {})
    return {
        "SYP": rates.get("SYP"),
        "EUR": rates.get("EUR")
    }


print(price())
	