import requests
import time
from multiprocessing import Process, Queue

coin_name = "KRW-"
desired_percent = 0


def ticker(coin_name):
    coin_name = "KRW-"+coin_name
    url = "https://api.upbit.com/v1/ticker"
    res = requests.request("GET", url, params={"markets":coin_name})
    return res.json()


def loop_limit(desired_price, coin):
    response = ticker(coin)
    present_price = float(response[0]['trade_price'])
    if desired_price >= present_price:
        print("하한선에 도착하였습니다.")
        exit()
    print("현재 가격: "+str(present_price))
    time.sleep(10)


if __name__ == "__main__":
    coin_name += input("코인 이름을 약어로 입력하시오. ex)BTC\n")
    desired_percent = float(input("하한선을 퍼센트로 입력하시오.\n"))
    response = ticker(coin_name)
    start_price = float(response[0]['trade_price'])
    desired_price = (start_price / 100) * (100-desired_percent)
    pr1 = Process(target=loop_limit, args=(desired_price, coin_name))
    pr1.start()
    pr1.join()