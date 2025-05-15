from datetime import datetime
import requests
from collections import Counter

class SalesManager:
    def __init__(self, api_url):
        self.api_url = api_url

    def get_today_sales(self, today_date):
        try:
            res = requests.get(f"{self.api_url}/sales")
            if res.status_code == 200:
                all_sales = res.json()
                today_sales = [
                    s for s in all_sales if s["timestamp"].startswith(today_date)
                ]
                return today_sales
            return []
        except Exception as e:
            print("Error fetching sales:", e)
            return []

    def add_sale(self, product, price, quantity, timestamp):
        try:
            sale_data = {
                "product": product,
                "price": price,
                "quantity": quantity,
                "timestamp": timestamp
            }
            res = requests.post(f"{self.api_url}/sales", json=sale_data)
            return res.status_code == 201
        except Exception as e:
            print("Error adding sale:", e)
            return False

    def get_price_frequency(self, product):
        try:
            res = requests.get(f"{self.api_url}/sales")
            if res.status_code == 200:
                sales = res.json()
                return dict(Counter(
                    s["price"] for s in sales if s["product"] == product
                ))
            return {}
        except Exception as e:
            print("Error getting price frequency:", e)
            return {}
