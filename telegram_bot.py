import telegram
from telegram.ext import Updater, CommandHandler
from command_function import command_buy_sell
from multiprocessing import Process, Manager
from multiprocessing.managers import shared_memory
import time

f = open("./telegram_token.txt", 'r')
a = open("./access_key.txt", 'r')
s = open("./secret_key.txt", 'r')

telegram_token = f.readline()
access_key = a.readline()
secret_key = s.readline()
server_url = 'https://api.upbit.com'



class CommandFunctions:

    def bot_init(self, update, context):
        self.id = update.effective_chat['id']
        with open('oo.txt', 'w') as f:
            f.write(str(self.id))
        context.bot.send_message(chat_id=update.effective_chat.id, text="작동 시작합니다.")

    def bot_check(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="듣고 있습니다.")

    def bot_price(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="")

    def bot_buy(self, update, context):
        if len(context.args) != 2:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="(wanted price, coin name) 두 정보를 잘 입력했는지 확인해 주세요.")
        res = command_buy_sell(self.server_url, self.access_key, self.secret_key, "bid", "price", context.args)
        print(res.status_code)
        print(res.text)
        if res.status_code == 201:
            print(res.text)
            context.bot.send_message(chat_id=update.effective_chat.id, text="매수 완료")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="값을 확인해주세요")

    def bot_sell(self, update, context):
        if len(context.args) != 2:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="(wanted price, coin name) 두 정보를 잘 입력했는지 확인해 주세요.")
        # server_url, access_key, secret_key, user_price, bid, coin
        res = command_buy_sell(self.server_url, self.access_key, self.secret_key, "ask", "market", context.args)
        if res.status_code == 201:
            print(res.text)
            context.bot.send_message(chat_id=update.effective_chat.id, text="매도 완료")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="매도 완료")

    def bot_stop(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="")

    def bot_limitsetup(self, update, context):

        context.bot.send_message(chat_id=update.effective_chat.id, text="")


class InputHandler(CommandFunctions):
    def make_handler(self):
        self.handler.append(CommandHandler('start', self.bot_init))
        self.handler.append(CommandHandler('check', self.bot_check))
        self.handler.append(CommandHandler('price', self.bot_price))
        self.handler.append(CommandHandler('buy', self.bot_buy))
        self.handler.append(CommandHandler('sell', self.bot_sell))
        self.handler.append(CommandHandler('stop', self.bot_stop))
        self.handler.append(CommandHandler('limitsetup', self.bot_limitsetup))

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


def xx():
    global telegram_token
    global TelegramBot

    x_bot = TelegramBot(telegram_token)
    while True:
        try:
            with open('oo.txt','r') as f:
                word = f.readline()
            x_bot.core.send_message(chat_id=word, text="1")
        except:
            pass
        time.sleep(10)

if __name__ == "__main__":
    bot = TelegramBot(telegram_token)
    th1 = Process(target=xx, args=())
    th1.start()
    bot.start()

