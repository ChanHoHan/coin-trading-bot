import telegram
from telegram.ext import Updater, CommandHandler

telegram_token = ""

class SendMessage():
    def bot_init(self, update, context):
        self.id = update.effective_chat
        context.bot.send_message(chat_id = update.effective_chat.id, text="작동 시작합니다.")

    def bot_check(self, update, context):
        context.bot.send_message(chat_id = update.effective_chat.id, text="듣고 있습니다.")

    def bot_price(self, update, context):
        context.bot.send_message(chat_id = update.effective_chat.id, text="")

    def bot_buy(self, update, context):
        context.bot.send_message(chat_id = update.effective_chat.id, text="")
    
    def bot_sell(self, update, context):
        context.bot.send_message(chat_id = update.effective_chat.id, text="")
        
    def bot_stop(self, update, context):
        context.bot.send_message(chat_id = update.effective_chat.id, text="")
    
    def bot_limitsetup(self, update, context):
        context.bot.send_message(chat_id = update.effective_chat.id, text="")


class InputHandler(SendMessage):
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
        self.id = ""
        self.handler = []
        self.make_handler()
        self.dispatch_handler(self.updater.dispatcher)

    def start(self):
        self.updater.start_polling()
        self.updater.idle()

    def sendMessage(self, text):
        self.core.sendMessage(chat_id=self.id, text=text)


if __name__ == "__main__":
    bot = TelegramBot(telegram_token)
    bot.start()
