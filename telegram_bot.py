import telegram
from telegram.ext import Updater, CommandHandler
from command_function import command_buy_sell

f = open("./telegram_token.txt", 'r')
a = open("./access_key.txt", 'r')
s = open("./secret_key.txt", 'r')

telegram_token = f.readline()
access_key = a.readline()
secret_key = s.readline()
server_url = 'https://api.upbit.com'


class CommandFunctions:
    def __init__(self):
        self.id = ""

    def bot_init(self, update, context):
        self.id = update.effective_chat
        context.bot.send_message(chat_id=update.effective_chat.id, text="작동 시작합니다.")

    def bot_check(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="듣고 있습니다.")

    def bot_price(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="")

    def bot_buy(self, update, context):
        global access_key
        global secret_key
        global server_url

        if len(context.args) != 3:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="(wanted price, buy/sell, coin name) 세 정보를 잘 입력했는지 확인해 주세요.")
        # server_url, access_key, secret_key, user_price, bid, coin
        res = command_buy_sell(server_url, access_key, secret_key, context.args)
        print(res.state)
        context.bot.send_message(chat_id=update.effective_chat.id, text="매수 완료")

    def bot_sell(self, update, context):
        global access_key
        global secret_key
        global server_url

        if len(context.args) != 3:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="(wanted price, buy/sell, coin name) 세 정보를 잘 입력했는지 확인해 주세.")
        # server_url, access_key, secret_key, user_price, bid, coin
        res = command_buy_sell(server_url, access_key, secret_key, context.args)
        command_buy_sell(server_url, access_key, secret_key, context.args)
        context.bot.send_message(chat_id=update.effective_chat.id, text="")

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
    def __init__(self, token):
        self.core = telegram.Bot(token)
        self.updater = Updater(token=token, use_context=True)
        self.handler = []
        self.make_handler()
        self.dispatch_handler(self.updater.dispatcher)

    def start(self):
        self.updater.start_polling()
        self.updater.idle()


if __name__ == "__main__":
    bot = TelegramBot(telegram_token)
    bot.start()
