import sys
sys.path.append('.')

import okx.Trade as Trade
import time
import datetime
from config import Config as config

api_key = config.API_KEY
api_secret_key = config.API_SECRET_KEY
passphrase = config.PASSPHRASE

proxy = 'http://127.0.0.1:7078'

tradeApi = Trade.TradeAPI(api_key=api_key, api_secret_key=api_secret_key, passphrase=passphrase, proxy=proxy,
                          flag=config.FLAG)


def buy_by_market():
    result = tradeApi.place_order(
        instId=config.INST_ID,
        tdMode="cash",
        side="buy",
        ordType="market",
        sz=config.USDT_NUM,
        clOrdId=config.CL_OID
    )
    if result["code"] == '0':
        print("Place order successfully. Result:%s" % result)
    else:
        print("Place order failed. Result: %s" % result)


def sell_by_market(result):
    num = get_order_num(result)
    num = str(float(num) * 99.8 / 100)
    result1 = tradeApi.place_order(
        instId=config.INST_ID,
        tdMode="cash",
        side="sell",
        ordType="market",
        sz=num
    )
    if result1["code"] == '0':
        print("Place order successfully. Result:%s" % result1)
    else:
        print("Place order failed. Result: %s" % result1)

def buy_by_limit():
    result = tradeApi.place_order(
        instId=config.INST_ID,
        tdMode="cash",
        side="buy",
        ordType="limit",
        sz=config.COIN_NUM,
        clOrdId=config.CL_OID,
        px=config.PRICE
    )
    if result["code"] == '0':
        print("Place order successfully. Result:%s" % result)
    else:
        print("Place order failed. Result: %s" % result)

def sell_by_limit(result):
    num = get_order_num(result)
    num = str(float(num) * 99.8 / 100)
    price = get_order_price(result)
    price = str(float(price) * config.TIMES)
    result1 = tradeApi.place_order(
        instId=config.INST_ID,
        tdMode="cash",
        side="sell",
        ordType="limit",
        sz=num,
        px=price
    )
    if result1["code"] == '0':
        print("Place order successfully. Result:%s" % result1)
    else:
        print("Place order failed. Result: %s" % result1)


def order_list():
    result = tradeApi.get_orders_history(
        instType="SPOT",
        ordType="market,limit"
    )
    print(result)


def order_info():
    result = tradeApi.get_order(
        instId=config.INST_ID,
        clOrdId=config.CL_OID
    )
    print(result)
    return result


def get_order_num(result):
    num = result['data'][0]['fillSz']
    print("成交数量:%s" % num)
    return num


def get_order_price(result):
    price = result['data'][0]['fillPx']
    print('成交价格：%s' % price)
    return price


def main():
    if not config.INSTANT_TRADE:
        print("配置的运行时间为：%s" % config.START_TIME)
        now = datetime.datetime.now()
        while now.strftime("%H:%M:%S") < config.START_TIME:
            now = datetime.datetime.now()
            time.sleep(0.0001)
    # buy_by_market()
    buy_by_limit()
    time.sleep(2)
    result = order_info()
    # sell_by_limit(result)
    # sell_by_market(result)


if __name__ == '__main__':
    main()
