#!/usr/bin/env python3

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import config

import unittest
import exmo

class TestExmo(unittest.TestCase):
    
    exchange = exmo.Exmo(
        api_key = config.settings['exchanges']['exmo']['api_key'],
        api_secret = config.settings['exchanges']['exmo']['api_secret'],
    )

    # Init
    def test_init(self):
        self.assertIsNotNone(self.exchange.http)
    
    
    # Recent trades
    def test_trades(self):
        pair = ['BTC','USD']
        limit = 1234
        trades = self.exchange.get_trades(pair[0], pair[1], limit)
        self.assertEqual(len(trades), limit)
        
    # Order book
    def test_orders(self):
        pair = ['BTC','USD']
        orders = self.exchange.get_orders(pair[0], pair[1])
        self.assertEqual(len(orders[pair[0]+'_'+pair[1]]['ask']), 100)
        
    # Ticker
    def test_ticker(self):
        ticker = self.exchange.get_ticker()
        self.assertEqual(len(ticker), 13)
        ticker
        
    # Currency pair settings
    def test_pairs(self):
        pairs = self.exchange.get_pairs()
        self.assertEqual(len(pairs), 13)
        
    # Currency list
    def test_currencies(self):
        currencies = self.exchange.get_currencies()
        self.assertEqual(len(currencies), 8)
        
        
    # Currency balances
    def test_balances(self):
        balances = self.exchange.get_balances()
        self.assertEqual(len(balances), 8)
        
    # Create an order that won't go through, then cancel it
    def test_order_create(self):
        pair = ['DOGE','BTC']
        # sell 100 DOGE at 0.1 BTC/DOGE
        # surely, noone will pay tha price, so the order can be cancelled
        response = self.exchange.order_create(pair[0], pair[1], quantity=100, price=0.1, type='sell')
        self.assertTrue(response['result'])
        if not response['result']:
            print(response['error'])
        else:
            cancel_response = self.exchange.order_cancel(response['order_id'])
            self.assertTrue(cancel_response['result'])
                    
if __name__ == '__main__':
    unittest.main()
