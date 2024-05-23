from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import logging
from googleapi import listTaskList ,getTaskFromList

# Replace with your actual token
token = '7138018453:AAHlrep8ra64s_Sfimn4wzgXgmZhyXto7KQ'
#
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# logger = logging.getLogger(__name__)

def start(update, context):
    user_id = update.message.from_user.id
    context.bot.send_message(chat_id=user_id, text="Hello! Welcome to the bot.")
    update.message.reply_text(f'Hello! {user_id}, I can help you manage your Google tasks.', reply_markup=main_keyboard())

def main_keyboard():
    keyboard = [['See All Tasks']]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

def header_tasks(task_list):
    # Create an inline keyboard with tasks dynamically
    keyboard = [
        [InlineKeyboardButton(task[0], callback_data=f"{task[0]}|{task[1]}")]
         for task in task_list]
    return InlineKeyboardMarkup(keyboard)

def main_menu(update, context):
    update.message.reply_text('Main Menu:', reply_markup=main_keyboard())

def handle_messages(update, context):
    text = update.message.text
    if text == 'See All Tasks':
        # Handle showing all tasks
        update.message.reply_text('Fetching all your tasks...')
        task_list = listTaskList()  # Assuming this function returns a list of tuples (task_name, task_id)
        if task_list:
            update.message.reply_text('Here are all your tasks:', reply_markup=header_tasks(task_list))
        else:
            update.message.reply_text('No tasks found.')
    else:
        update.message.reply_text('Sorry, I didn\'t understand that command.')

def button(update, context):
    query = update.callback_query
    query.answer()
    callback_data = query.data
    task_name, task_id = callback_data.split('|')
    detail_tasks = getTaskFromList(task_id, False)
    pretext = (f"---{task_name}---\n")
    if not detail_tasks:
        message_text = f"{task_name}:\nNo details found for this task."
    else:
        message_text = f"\n".join(str(i[0]) for i in detail_tasks)

    query.edit_message_text(text=pretext + message_text)


def main():
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_messages))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
