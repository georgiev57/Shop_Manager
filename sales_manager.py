import requests
from collections import Counter

class SalesManager:
    def __init__(self, api_url):
        self.api_url = api_url

    def add_sale(self, item, price, quantity, timestamp):
        res = requests.post(f"{self.api_url}/sales", json={
            "product": item,
            "price": price,
            "quantity": quantity,
            "timestamp": timestamp
        })
        return res.status_code == 201

    def get_sales(self):
        res = requests.get(f"{self.api_url}/sales")
        if res.status_code == 200:
            return res.json()
        return []

    def get_today_sales(self, date_prefix):
        return [s for s in self.get_sales() if s["timestamp"].startswith(date_prefix)]

    def get_price_frequency(self, item):
        prices = [s["price"] for s in self.get_sales() if s["product"] == item]
        return dict(Counter(prices))
