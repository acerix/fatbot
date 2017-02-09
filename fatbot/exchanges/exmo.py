
import hashlib
import hmac
import time
import json
import requests
import urllib

class Exmo():
    
    api_url = 'https://api.exmo.com/v1/'
    
    buy_commission = 0.002
    
    def __init__(self, api_key=None, api_secret=None):
        
        self.api_key = api_key
        self.api_secret = api_secret
        self.http = requests.Session()

        
    def request(self, path, params={}, auth=False):
        
        if auth:
        
            params['nonce'] = int(round(time.time()*1000))
            
            encoded_params = urllib.parse.urlencode(params)
        
            request_hmac = hmac.new(
                str.encode(self.api_secret),
                str.encode(encoded_params),
                hashlib.sha512
            )
            
            self.http.headers.update({
                'Content-type': 'application/x-www-form-urlencoded',
                'Key': self.api_key,
                'Sign': request_hmac.hexdigest()
            })
            
            request = self.http.post(self.api_url + path, data=encoded_params)
        
        else:
            
            if len(params):
                path = path + '?' + urllib.parse.urlencode(params)
            
            request = self.http.get(self.api_url + path)
        
        return request.json()
        
        
    def get_trades(self, currency_1_code, currency_2_code, limit=10000):
        pair = currency_1_code+'_'+currency_2_code
        return self.request('trades', {'pair': pair, 'limit': limit})[pair]

    def get_orders(self, currency_1_code, currency_2_code):
        return self.request('order_book', {'pair': currency_1_code+'_'+currency_2_code})
        
    def get_ticker(self):
        return self.request('ticker')

    def get_pairs(self):
        return self.request('pair_settings')

    def get_currencies(self):
        return self.request('currency')
        
    def get_balances(self):
        
        user_info = self.request('user_info', auth=True)
        
        if 'balances' in user_info:
            return user_info['balances']
            
        print(user_info)
        raise Exception('Error getting balances')

    def order_create(self, currency_1_code, currency_2_code, quantity, price, type):
        return self.request('order_create', {
            'pair': currency_1_code+'_'+currency_2_code,
            'quantity': quantity,
            'price': price,
            'type': type
        }, auth=True)
        
    def order_cancel(self, order_id):
        return self.request('order_cancel', {
            'order_id': order_id
        }, auth=True)
        
