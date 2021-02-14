import requests
from time import sleep
from multiprocessing import Process, Queue

desired_percent = 0


def ticker(coin_name):
    url = "https://api.upbit.com/v1/ticker"
    res = requests.request("GET", url, params={"markets": "{}".format(coin_name)})
    return res.json()


def my_multiprocess():
    coin_name = "KRW-"
    flag = False
    while not flag:
        file_input = open("./input.txt", 'r')
        input_lines = file_input.readlines()
        if len(input_lines) == 2:
            coin_name = coin_name + input_lines[0]
            limit = float(input_lines[1])
            res = ticker(coin_name)
            start_price = float(res[0]['trade_price'])
            while True:
                res = ticker(coin_name)
                present_price = res[0]["trade_price"]
                file_output = open("./output.txt", 'w')
                file_output.write(str(present_price))
                print(present_price)
                file_output.close()
                desired_price = (start_price / 100) * (100 - limit)
                if desired_price >= present_price:
                    print("하한선에 도착하였습니다.")
                    file_output = open("./output.txt", 'w')
                    file_output.write("end")
                    file_output.close()
                    flag = True
                    break
                sleep(10)
        file_input.close()
        sleep(10)


if __name__ == "__main__":
    pr1 = Process(target=my_multiprocess)
    pr1.start()
    pr1.join()