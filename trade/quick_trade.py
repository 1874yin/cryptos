import okx.Trade as Trade
import okx.PublicData as PublicData
import time
import datetime
import Config as config

api_key = config.API_KEY
api_secret_key = config.API_SECRET_KEY
passphrase = config.PASSPHRASE

tradeApi = Trade.TradeAPI(api_key=api_key, api_secret_key=api_secret_key, passphrase=passphrase, proxy=config.PROXY, flag=config.FLAG)

def buy_by_market():
    result = tradeApi.place_order(
        instId=config.INST_ID,
        tdMode="cash",
        side="buy",
        ordType="market",
        sz=config.USDT_NUM,
        clOrdId=config.CL_ORDID
    )
    if result["code"] == '0':
        print("Place order successfully. Result:%s" % result)
    else:
        print("Place order failed. Result: %s" % result)

def sell_by_market(result):
    num = get_order_num(result)
    num = str(float(num) * 99.8 / 100)
    result = tradeApi.place_order(
        instId=config.INST_ID,
        tdMode="cash",
        side="sell",
        ordType="market",
        sz=num
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
    result = tradeApi.place_order(
        instId=config.INST_ID,
        tdMode="cash",
        side="sell",
        ordType="limit",
        sz=num,
        px=price
    )

def order_list():
    result = tradeApi.get_orders_history(
        instType="SPOT",
        ordType="market,limit"
    )
    print(result)

def order_info():
    result = tradeApi.get_order(
        instId=config.INST_ID,
        clOrdId=config.CL_ORDID
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
    buy_by_market()
    time.sleep(2)
    # sell_by_market()
    result = order_info()
    sell_by_limit(result)
    
    
if __name__ == '__main__':
    main()