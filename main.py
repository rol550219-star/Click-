import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# 1. Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = "8685276551:AAHaWurnWMqaxPMx8_GhyqG9DQ4iQdtO06E"

# Словарь для сохранения баланса игроков
scores = {}

# Команда /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 Добро пожаловать в кликер!\n\n"
        "Натапай **500 очков**, чтобы пройти первый этап (после этого баланс сбросится на 0, и можно будет тапать бесконечно).\n"
        "Введи команду **/gameclicker**, чтобы открыть игровую панель.",
        parse_mode='Markdown'
    )


# Команда /gameclicker — выводит сообщение с кнопкой TAP
async def gameclicker_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id not in scores:
        scores[user.id] = 0

    current_score = scores[user.id]

    keyboard = [
        [InlineKeyboardButton("👆 TAP", callback_data="click_action")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if current_score > 500:
        text = f"🏆 **Твой кликер**\n\nБаланс: **{current_score}** очков (свободный режим)"
    else:
        text = f"🏆 **Твой кликер**\n\nБаланс: **{current_score} / 500** очков"

    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')


# Обработчик нажатия на кнопку TAP
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    if user.id not in scores:
        scores[user.id] = 0

    scores[user.id] += 1
    current_score = scores[user.id]

    if current_score == 500:
        scores[user.id] = 0
        await query.edit_message_text(
            f"🎉 Поздравляем, @{user.username or user.first_name}!\n\n"
            "Ты натапал **500 очков**! Твой баланс сброшен на 0, теперь можешь тапать дальше сколько угодно.",
            parse_mode='Markdown'
        )
        return

    if current_score > 500:
        text = f"🏆 **Твой кликер**\n\nБаланс: **{current_score}** очков (свободный режим)"
    else:
        text = f"🏆 **Твой кликер**\n\nБаланс: **{current_score} / 500** очков"

    keyboard = [
        [InlineKeyboardButton("👆 TAP", callback_data="click_action")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')


# Главная функция запуска
if __name__ == '__main__':
    print("Бот-кликер запускается...")
    
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('gameclicker', gameclicker_command))
    application.add_handler(CallbackQueryHandler(button_handler, pattern="click_action"))

    print("Бот работает!")
    application.run_polling()
    
