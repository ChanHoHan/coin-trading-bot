import requests
import time

coin_name = "KRW-"
desired_percent = 0

def ticker(coin_name):
    coin_name = "KRW-"+coin_name
    url = "https://api.upbit.com/v1/ticker"
    res = requests.request("GET", url, params={"markets":coin_name})
    return res.json()

if __name__ == "__main__":
    coin_name += input("코인 이름을 약어로 입력하시오. ex)BTC\n")
    desired_percent = float(input("하한선을 퍼센트로 입력하시오.\n"))
    response = ticker()
    start_price = float(response[0]['trade_price'])
    desired_price = (start_price / 100) * (100-desired_percent)
    print(start_price)
    print(desired_price)
    while True:
        response = ticker()
        present_price = float(response[0]['trade_price'])
        if (desired_price >= present_price):
            break
        print(present_price)
        time.sleep(10)