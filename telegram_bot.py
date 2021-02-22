import telegram
import requests
from time import sleep
import json
from telegram.ext import Updater, CommandHandler
from command_function import command_buy_sell
from multiprocessing import Process, Manager, Queue
import time
import os

f = open("./telegram_token.txt", 'r')
a = open("./access_key.txt", 'r')
s = open("./secret_key.txt", 'r')

telegram_token = f.readline()
access_key = a.readline()
secret_key = s.readline()
server_url = 'https://api.upbit.com'

def ticker(coin_name):  # upbit에서 가격 정보 얻어오는 함수
    url = "https://api.upbit.com/v1/ticker"
    try:
        res = requests.request("GET", url, params={"markets": coin_name})
        res = res.json()
        res[0]['trade_price']  # 오류 처리 위해서 res 리스트 속 trade_price 인자가 존재하는지 확인
        return res
    except:
        error = "error"
        return error  # 위에 확인 구문에서 오류 탐지하고 error 반환

def file_change_check(input_lines):  # input.txt 속 내용이 바뀌었는지 확인하는 함수
    try:
        change_file = open("./input.txt", 'r')
        change_lines = change_file.readlines()
        change_file.close()
        if (len(change_lines) != 2):
            return change_lines
        if change_lines[0] != input_lines[0] or change_lines[1] != input_lines[1]:
            return change_lines
        return False
    except:
        return False
        # input.txt를 읽어오지 못했거나, 읽어온 input.txt를 저장한 리스트 값에 문제가 생기면 False 리턴
        # False를 리턴해서 그냥 넘기고 나면 my_multiprocess 함수 내에서 다시 확인 후 처리해주는 구문 있음

def multiprocess_init():
    try:
        os.remove(input.txt)
    except:
        pass
    while True:
        try:
            with open('./bot_id.txt', 'r') as f:  # init(/start)으로 bot_id.txt 생성하면 시작하도록 함
                word = f.readline()
            break
        except:
            pass
        sleep(0.5)

    with open('./input.txt', "w") as f:
        f.write("init\n")
        f.write("setup")
    return word


def stop_check():
    try:
        with open("./stop.txt", 'r') as file_stop:
            stop = file_stop.readlines()
            file_stop.close()
            os.remove("./stop.txt")
            if stop[0] == "stop":
                return 0
            return 1
    except:
        return 1


def my_multiprocess():
    global telegram_token
    global TelegramBot
    stop_flag = 1

    x_bot = TelegramBot(telegram_token)
    word = multiprocess_init()

    input_file = open("./input.txt", 'r')
    input_lines = input_file.readlines()
    input_file.close()
    while stop_flag:
        while stop_flag:
            stop_flag = stop_check()
            tmp = file_change_check(input_lines)# 하한선에 도달하였거나 잘못된 input.txt 값이 들어온 경우 input.txt값이 바뀔때까지 기다렸다가 다시 처음부터 실행
            if (tmp):
                input_lines = tmp
                break
            else:
                pass
            sleep(0.5)
        if len(input_lines) == 2:  # input.txt 속 내용이 형식에 맞는 경우 실행되는 if문
            coin_name = "KRW-" + input_lines[0]  # 코인 이름
            limit = float(input_lines[1])  # 코인 하한가 퍼센트
            res = ticker(coin_name)  # 코인 값 가져옴
            if res == "error":  # ticker 함수에서 error 반환했을때 처리
                x_bot.core.send_message(chat_id=word, text="코인 이름을 다시 확인해주세요.")
                break
            start_price = float(res[0]['trade_price'])  # 시작 가격 저장
            while stop_flag:
                stop_flag = stop_check()
                if file_change_check(input_lines):  # input.txt 파일 내용이 바뀌었는지 확인(중간에 /limitsetup 다시 써서 변화한경우 등등)
                    x_bot.core.send_message(chat_id=word, text="값 변경이 확인되었습니다.")
                    break
                res = ticker(coin_name)
                if res == "error":
                    x_bot.core.send_message(chat_id=word, text="코인 이름을 다시 확인해주세요.")
                    break
                present_price = res[0]["trade_price"]
                if stop_flag:
                    x_bot.core.send_message(chat_id=word, text="{}".format(str(present_price)))
                desired_price = (start_price / 100) * (100 - limit)
                if desired_price >= present_price:
                    x_bot.core.send_message(chat_id=word, text="하한선에 도달하였습니다.")
                    x_bot.core.send_message(chat_id=word, text="새로운 값을 입력해주세요.")
                    break
                sleep(10)
        else: # input.txt파일이 정 
            x_bot.core.send_message(chat_id=word, text="형식에 맞게 /limitsetup 을 다시 설정하십시오.")


class CommandFunctions:
    def bot_init(self, update, context):
        self.id = update.effective_chat['id']
        with open('bot_id.txt', 'w') as f:
            f.write(str(self.id))
        context.bot.send_message(chat_id=update.effective_chat.id, text="작동 시작합니다.")

    def bot_check(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="듣고 있습니다.")

    def bot_price(self, update, context):
        coin_name = "KRW-" + context.args[0]
        res = ticker(coin_name)
        coin_price = float(res[0]['trade_price'])
        context.bot.send_message(chat_id=update.effective_chat.id, text="{}".format(coin_price))

    def bot_buy(self, update, context):
        if len(context.args) != 2:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="(wanted price, coin name) 두 정보를 잘 입력했는지 확인해 주세요.")
        res = command_buy_sell(self.server_url, self.access_key, self.secret_key, "bid", "price", context.args)
        text = json.loads(res.text)
        if res.status_code == 201:
            context.bot.send_message(chat_id=update.effective_chat.id, text="매수 완료")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=text["error"]["message"])

    def bot_sell(self, update, context):
        if len(context.args) != 2:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="(wanted price, coin name) 두 정보를 잘 입력했는지 확인해 주세요.")
        # server_url, access_key, secret_key, user_price, bid, coin
        res = command_buy_sell(self.server_url, self.access_key, self.secret_key, "ask", "market", context.args)
        text = json.loads(res.text)
        if res.status_code == 201:
            context.bot.send_message(chat_id=update.effective_chat.id, text="매도 완료")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=text["error"]["message"])

    def bot_stop(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="종료 완료")
        file_stop = open("./stop.txt", 'w')
        file_stop.write("stop")
        file_stop.close()
        self.updater.dispatcher.stop()
        self.updater.job_queue.stop()
        self.updater.stop()

    def bot_limitsetup(self, update, context):
        file_input = open("./input.txt", 'w')
        file_input.write(context.args[0])
        file_input.write("\n")
        file_input.write(context.args[1])
        file_input.close()
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="{} 코인 / 하한가 {} % 설정완료".format(context.args[0], context.args[1]))

    def bot_help(self, update, context):
        help_text = "/start : telegram bot token이 필요하므로, /start 명령어를 필수적으로 입력해 줍니다.\n\n /stop : 현재 작동중인 프로그램을 멈춥니다. \n\n /limitsetup [코인 심볼] [하한가(%)] : 원하는 코인이 지정한 하한가에 도달했을 경우 위 사진 처럼 알람이 울립니다. \n\n /sell [코인 심볼] [원하는 코인의 총 수량] : 원하는 코인을 원하는 총 수량만큼 시장 가격으로 매도합니다. \n\n /buy [코인 심볼] [원하는 총 가격] : 원하는 코인을 원하는 총 가격 만큼 시장 가격으로 매수합니다. \n\n /price [코인 심볼] : 원하는 코인의 가격을 확인합니다. "
        context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

class InputHandler(CommandFunctions):
    def make_handler(self):
        self.handler.append(CommandHandler('start', self.bot_init))
        self.handler.append(CommandHandler('check', self.bot_check))
        self.handler.append(CommandHandler('price', self.bot_price))
        self.handler.append(CommandHandler('buy', self.bot_buy))
        self.handler.append(CommandHandler('sell', self.bot_sell))
        self.handler.append(CommandHandler('stop', self.bot_stop))
        self.handler.append(CommandHandler('limitsetup', self.bot_limitsetup))
        self.handler.append(CommandHandler('help', self.bot_help))

    def dispatch_handler(self, dispatcher):
        for element in self.handler:
            dispatcher.add_handler(element)


class TelegramBot(InputHandler):
    global access_key
    global secret_key
    global server_url

    def __init__(self, token):
        self.id = ""
        self.core = telegram.Bot(token)
        self.updater = Updater(token=token, use_context=True)
        self.handler = []
        self.make_handler()
        self.dispatch_handler(self.updater.dispatcher)
        self.access_key = access_key
        self.secret_key = secret_key
        self.server_url = server_url

    def start(self):
        self.updater.start_polling()
        self.updater.idle()


if __name__ == "__main__":
    pr1 = Process(target=my_multiprocess)
    pr1.start()
    bot = TelegramBot(telegram_token)
    bot.start()
