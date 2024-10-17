import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler
import requests

# إعدادات التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# توكن البوت
TOKEN = '6311584133:AAEBIa3t5bCAic1MH_ayqcVQ9crem_Qx91M'
# توكن DeepL API
DEEPL_API_KEY = 'edb869d4-02fc-4981-b531-344a03dd21b8:fx'
DEEPL_API_URL = 'https://api-free.deepl.com/v2/translate'

# معرف المستخدم الخاص بك
YOUR_USER_ID = 1693067897  # استبدل هذا بمعرف المستخدم الخاص بك

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='أهلاً بك! أرسل لي أي نص لأترجمه إلى العربية.')

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
        logging.error(f"Error in translation: {response.status_code} - {response.text}")
        return "حدث خطأ أثناء الترجمة."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == YOUR_USER_ID:  # تحقق من معرف المستخدم
        text = update.message.text
        translated_text = translate_text(text)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=translated_text)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='آسف، لا يمكنك استخدام هذا البوت.')

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(echo_handler)

    application.run_polling()
