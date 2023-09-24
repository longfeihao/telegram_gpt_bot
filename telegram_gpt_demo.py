import logging

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


from file_utils import load_bot_conf
from gpt_utils import gpt_35_api_completion, get_models


MESSAGES = []
MODEL = 'gpt-3.5-turbo-0613'


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    global MESSAGES
    MESSAGES = []
    await update.message.reply_text("Clear!")


async def listmodel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    global MODEL
    available_models = '\n'.join([f'- {e}' for e in get_models()])

    cur_model = MODEL

    info = f"""Available Model:
{available_models}

Current Model:
{cur_model}
    """

    await update.message.reply_text(info)


async def setmodel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    args = context.args
    if len(args) == 0:
        await update.message.reply_text("Please input model name!")
        return

    valid_models = set(get_models())

    if args[0] not in valid_models:
        await update.message.reply_text("Invalid model name!")
        return
    else:
        global MODEL
        MODEL = args[0]
        await update.message.reply_text("Set model to " + MODEL + "!")


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    text = update.message.text
    global MESSAGES
    MESSAGES.append({'role': 'user','content': text})
    response_text = gpt_35_api_completion(MESSAGES, MODEL)
    MESSAGES.append({'role': 'assistant','content': response_text})

    await update.message.reply_text(response_text)


def main(token) -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clear", clear_command))
    application.add_handler(CommandHandler("listmodel", listmodel_command))
    application.add_handler(CommandHandler("setmodel", setmodel_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    bot_conf = load_bot_conf()
    token = bot_conf['token']
    main(token)
