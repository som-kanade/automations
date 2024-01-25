import requests
import time
from prometheus_client import start_http_server, Gauge
start_http_server(8000)

price_difference_metric = Gauge('crypto_price_difference', 'Price difference for top cryptocurrencies', ['crypto_id'])


# Method to Get API response 
def fetch_crypto_prices():
    api_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
    response = requests.get(api_url)

    if response.status_code == 200:
        data =  response.json()
        return data
    else:
        print(f"Error: {response.status_code}")
        return None

# Method to update prometheus metrics
def update_prometheus_metrics(output):
    for crypto_id, price_difference in output.items():
        price_difference_metric.labels(crypto_id).set(price_difference)


def main():
    prices_data_old = {}
    while True:
        prices_data = fetch_crypto_prices()
        
        if prices_data_old: 
            old_price_mapping = {}
            for data in prices_data_old:
                old_price_mapping[data['id']] = data['current_price']

            diff_mapping = {}
            for data in prices_data:
                difference = abs(data['current_price'] - old_price_mapping[data['id']])
                diff_mapping[data['id']] = data['current_price']

            output = {}
            for current in sorted(diff_mapping.items(), key=lambda x: x[1], reverse=True)[:5]:
                output[current[0]] = current[1]
            print(output)
            #update_prometheus_metrics(output)
                

        prices_data_old = prices_data
        
        time.sleep(300)

if __name__ == "__main__":
    main()
