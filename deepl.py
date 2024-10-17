import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

# إعدادات التسجيل
logging.basicConfig(format='%(asctime)s - %(name__) - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# توكن البوت
TOKEN = '7190727472:AAEl3Et2eL8VP0CwVIIGTsRhD6xRd6vHINw'
# توكن DeepL API
DEEPL_API_KEY = 'edb869d4-02fc-4981-b531-344a03dd21b8:fx'
DEEPL_API_URL = 'https://api-free.deepl.com/v2/translate'

# معرف المستخدم الخاص بك
YOUR_USER_ID = 1693067897  # استبدل هذا بمعرف المستخدم الخاص بك

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('أهلاً بك! أرسل لي أي نص لأترجمه إلى العربية.')

def translate_text(text: str) -> str:
    params = {
        'auth_key': DEEPL_API_KEY,
        'text': text,
        'target_lang': 'AR'  # اللغة المستهدفة: العربية
    }
    response = requests.post(DEEPL_API_URL, data=params)
    if response.status_code == 200:
        return response.json()['translations'][0]['text']
    else:
        logger.error(f"Error in translation: {response.status_code} - {response.text}")
        return "حدث خطأ أثناء الترجمة."

def handle_message(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id == YOUR_USER_ID:  # تحقق من معرف المستخدم
        text = update.message.text
        translated_text = translate_text(text)
        update.message.reply_text(translated_text)
    else:
        update.message.reply_text('آسف، لا يمكنك استخدام هذا البوت.')

def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()