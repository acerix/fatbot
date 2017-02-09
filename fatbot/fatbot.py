#!/usr/bin/env python3

import config

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], 'exchanges'))
import exmo

import logging
import os
import time

def main():

    logging.basicConfig(
        filename = os.path.join(config.cache_dir, config.app_name + '.log'),
        level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s',
    )

    logging.info('Starting '+config.settings['bot']['name']+' version '+config.settings['bot']['version'])
    print('Starting '+config.settings['bot']['name']+' version '+config.settings['bot']['version'])

    exchange = exmo.Exmo(
        api_key = config.settings['exchanges']['exmo']['api_key'],
        api_secret = config.settings['exchanges']['exmo']['api_secret'],
    )
    
    # Run trade process in a loop
    while True:
    
        # For each currency with a balance
        for sell_currency_code, sell_currency_balance in exchange.get_balances().items():
            if float(sell_currency_balance) <= 0:
                continue
            
            print()
            print('Sell '+sell_currency_balance+' '+sell_currency_code+'?')
            
            # For each trading pair
            for trade_pair_code, trade_pair_info in exchange.get_pairs().items():
                
                # Codes are separated by an underscore with currency to sell first
                trade_sell_code, trade_buy_code = trade_pair_code.split('_')
                
                # If the pair is for selling this currency
                if sell_currency_code == trade_sell_code:
                    trade_sell_inverse = False
                    
                # If the pair is for buying this currency
                elif sell_currency_code == trade_buy_code:
                    trade_sell_inverse = True
                
                # If the pair is not for this currency
                else:
                    continue
               
                print(trade_sell_code, trade_buy_code, trade_sell_inverse)
            
            
            # Order tradable currencies by the probability price will go up .. ie. it is -1 if the price will surely go down, 1 if it will go up, 0 if price stays the same or unknown
                 
                # For each option while probability > 0.5 
                
                    # If expected profit > fees, create a trade order to sell



        # Delay before running again
        print()
        print('Sleeping for '+str(config.settings['bot']['trade_run_interval'])+'s')
        time.sleep(config.settings['bot']['trade_run_interval'])
    
# Handle Ctrl-C
import signal
import sys
def signal_handler(signal, frame):
    print()
    print('Stopping...')
    print()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    main()
