import telegram
from telegram.ext import Updater, CommandHandler


def command_check(self, update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="듣고 있습니다.")


def command_stop(self, update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="종료 완료")
    self.update.dispatcher.stop()
    self.update.job_queue.stop()
    self.update.stop()