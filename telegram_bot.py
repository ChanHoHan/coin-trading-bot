import telegram
from telegram.ext import Updater, CommandHandler

telegram_token = ""


class TelegramBot:
    def __init__(self, token):
        self.core = telegram.Bot(token)
        self.updater = Updater(token=token, use_context=True)
        self.id = ""

    def start(self):
        self.updater.start_polling()
        self.updater.idle()

    def sendMessage(self, text):
        self.core.sendMessage(chat_id=self.id, text=text)

    def o_start(self, update, context):
        self.id = update.effective_chat.id
        context.bot.send_message(chat_id=update.effective_chat.id, text=self.id)

if __name__ == "__main__":
    bot = TelegramBot(telegram_token)
    bot.start_handler = CommandHandler('start', bot.o_start)
    bot.updater.dispatcher.add_handler(bot.start_handler)
    bot.start()
