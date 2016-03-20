#!/usr/bin/env python3

import config

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], 'exchanges'))
import exmo



def get_trades():

    print('Spidering for new trades')
    
    db = config.db_connect()
    dbc = db.cursor()
    
    exchange = exchange = exmo.Exmo(
        api_key = config.settings['exchanges']['exmo']['api_key'],
        api_secret = config.settings['exchanges']['exmo']['api_secret'],
    )
    
    for (market_id, base_currency, trade_currency, trade_currency_divisor) in dbc.execute("""
SELECT
    market.id,
    base_currency.code,
    trade_currency.code,
    trade_currency.divisor
FROM
    market
JOIN
    currency base_currency
        ON
             base_currency.id = base_currency_id
JOIN
    currency trade_currency
        ON
             trade_currency.id = trade_currency_id
WHERE
    exchange_id = 1
""").fetchall():
    
        print(trade_currency, base_currency)
        
        for trade in exchange.get_trades(trade_currency, base_currency, 1000):
            
            dbc.execute("""
SELECT
    *
FROM
    trade
WHERE
    market_id = :market_id
AND
    trade_id = :trade_id
""",
{
    'market_id': market_id,
    'trade_id': trade['trade_id'],
})
            if dbc.fetchone() is None:
                
                dbc.execute("""
INSERT INTO
    trade
(
    market_id,
    price,
    amount,
    trade_id,
    trade_time
)
VALUES
(
    :market_id,
    :price,
    :amount,
    :trade_id,
    :trade_time
)
""",
{
    'market_id': market_id,
    'price': float(trade['price']),
    'amount': round( trade_currency_divisor * float(trade['quantity']) ),
    'trade_id': trade['trade_id'],
    'trade_time': trade['date']
})
                db.commit()


def main():

    print('Starting data spider')
    
    get_trades()
    
    
if __name__ == "__main__":
    main()
