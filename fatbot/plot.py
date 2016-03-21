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
    trade_id
FROM
    trade
WHERE
    market_id = :market_id
ORDER BY
    trade_id DESC
LIMIT
    :limit OFFSET :limit - 1
""",
{
    'market_id': market_id,
    'limit': limit
}).fetchone()

    c = 0
    for trade in dbc.execute("""
SELECT
    trade_id,
    price
FROM
    trade
WHERE
    market_id = :market_id
AND
    trade_id >= :trade_id
ORDER BY
    trade_id
""",
{
    'market_id': market_id,
    'trade_id': first_trade['trade_id']
}).fetchall():

        x.append(c)
        c = c + 1
        y.append(trade[1])

    return x, y

def recent_trade_plot(market_id, limit):

    x, y = recent_trade_points(market_id, limit)

    pylab.plot(x, y, 'o')
    pylab.show()


def main():
    recent_trade_plot(1, 500)

if __name__ == "__main__":
    main()

