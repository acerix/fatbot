#!/usr/bin/env python3

import config

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], 'exchanges'))
import exmo

import logging
import os
import time
import random

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
    
    trade_pairs = exchange.get_pairs();
    
    # Run trade process in a loop
    while True:
    
        # For each currency with a balance
        for sell_currency_code, sell_currency_balance in exchange.get_balances().items():
            if float(sell_currency_balance) <= 0:
                continue
            
            print()
            print('Sell '+sell_currency_balance+' '+sell_currency_code+'?')
            
            sell_options = []
            
            # Get list of options for selling this currency with the probability the buying price will go up
            for trade_pair_code, trade_pair_info in trade_pairs.items():
            
                # Codes are separated by an underscore with currency to sell first
                trade_sell_code, trade_buy_code = trade_pair_code.split('_')
                
                # If the pair is for selling this currency
                if sell_currency_code == trade_sell_code:
                    buy_currency_code = trade_buy_code
                    trade_sell_inverse = False
                    
                    if trade_pair_info['min_quantity'] > sell_currency_balance:
                        print('Cannot buy',buy_currency_code,'because the minimum quantity is',trade_pair_info['min_quantity'])
                        continue
                        
                    
                # If the pair is for buying this currency
                elif sell_currency_code == trade_buy_code:
                    buy_currency_code = trade_sell_code
                    trade_sell_inverse = True
                    
                    if trade_pair_info['min_amount'] > sell_currency_balance:
                        print('Cannot buy',buy_currency_code,'because the minimum amount is',trade_pair_info['min_amount'])
                        continue
                        
                
                # If the pair is not for this currency
                else:
                    continue
                
                
                # @todo ask a learner for a sell price and profit probability
                recommended_sell_price = trade_pair_info['max_price']
                profit_probability = random.random()
                
                if profit_probability < config.settings['bot']['probability_threshold']:
                    print('Skipping',buy_currency_code,'because the probability of profit is',profit_probability)
                    continue
                
                sell_options.append({
                    'buy_currency_code': buy_currency_code,
                    'trade_sell_inverse': trade_sell_inverse,
                    'profit_probability': profit_probability,
                    'trade_pair_info': trade_pair_info,
                    'recommended_sell_price': recommended_sell_price,
                })
                
            # Order tradable currencies by the probability price will go up ... ie. 1 if it will go up for sure, 0 if price has zero chance to go up
            sell_options = sorted(sell_options, key=lambda k: k['profit_probability'], reverse=True) 
            
            # Process sell options
            for sell_option in sell_options:
                
                # @todo calcuate actual estimates
                expected_profit = random.random()
                expected_fees = random.random()
                
                verb = 'Buy' if sell_option['trade_sell_inverse'] else 'Sell';
                
                print(verb+'ing',sell_option['buy_currency_code'],'at',sell_option['recommended_sell_price'],'has an expected value of',str(expected_profit - expected_fees))
                
                # If selling now looks profitable
                if expected_profit > expected_fees:
                    print('Sell sell sell!')
                
                else:
                    print('Skipping because expected value is not positive');
                    

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
