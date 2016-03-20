#!/usr/bin/env python3

import config
import pylab

def recent_trade_points(market_id, limit):

    db = config.db_connect()
    dbc = db.cursor()

    x = []
    y = []

    first_trade = dbc.execute("""
SELECT
    trade_time
FROM
    trade
WHERE
    market_id = :market_id
ORDER BY
    trade_time DESC
LIMIT
    :limit OFFSET :limit - 1
""",
{
    'market_id': market_id,
    'limit': limit
}).fetchone()

    
    for trade in dbc.execute("""
SELECT
    trade_time,
    price
FROM
    trade
WHERE
    market_id = :market_id
AND
    trade_time >= :trade_time
ORDER BY
    trade_time
""",
{
    'market_id': market_id,
    'trade_time': first_trade['trade_time']
}).fetchall():

        x.append(trade[0])
        y.append(trade[1])

    return x, y

def recent_trade_plot(market_id, limit):

    x, y = recent_trade_points(market_id, limit)

    pylab.plot(x, y, 'o')
    pylab.show()


def main():
    recent_trade_plot(1, 1000)

if __name__ == "__main__":
    main()

