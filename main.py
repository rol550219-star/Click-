import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# 1. Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Твой токен бота
TOKEN = "8709482604:AAEV1qPp4twI7wPpYRHyDxbhNqZzzEMTqSM"

# Словарь для сохранения баланса игроков (ключ — ID пользователя, значение — количество очков)
scores = {}


# Команда /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 Добро пожаловать в кликер!\n\n"
        "Введи команду **/gameclicker**, чтобы открыть игровую панель с кнопкой TAP.",
        parse_mode='Markdown'
    )


# Команда /gameclicker — выводит сообщение с кнопкой TAP
async def gameclicker_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id not in scores:
        scores[user.id] = 0

    current_score = scores[user.id]

    # Создаем клавиатуру с одной кнопкой TAP
    keyboard = [
        [InlineKeyboardButton("👆 TAP", callback_data="click_action")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем сообщение с балансом и кнопкой
    await update.message.reply_text(
        f"🏆 **Твой кликер**\n\nБаланс: **{current_score}** очков",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


# Обработчик нажатия на кнопку TAP
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() # Подтверждаем нажатие

    user = query.from_user
    if user.id not in scores:
        scores[user.id] = 0

    # Добавляем +1 очко
    scores[user.id] += 1
    current_score = scores[user.id]

    # Обновляем текст в сообщении с новым балансом
    keyboard = [
        [InlineKeyboardButton("👆 TAP", callback_data="click_action")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        f"🏆 **Твой кликер**\n\nБаланс: **{current_score}** очков",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


# Главная функция запуска
if __name__ == '__main__':
    print("Бот-кликер с кнопкой запускается...")
    
    application = ApplicationBuilder().token(TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('gameclicker', gameclicker_command))
    
    # Обработчик нажатий на инлайн-кнопки
    application.add_handler(CallbackQueryHandler(button_handler, pattern="click_action"))

    print("Бот работает!")
    application.run_polling()
                         
