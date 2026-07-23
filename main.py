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
        "Натапай **500 очков**, чтобы получить разбан (после этого баланс сбросится на 0).\n"
        "Введи команду **/gameclicker**, чтобы открыть игровую панель.",
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

    # Если игрок уже сбросил 500 и тапает дальше (бесконечно), показываем просто текущий баланс
    if current_score > 500:
        text = f"🏆 **Твой кликер**\n\nБаланс: **{current_score}** очков (разбан уже получен, тапай на будущее!)"
    else:
        text = f"🏆 **Твой кликер**\n\nБаланс: **{current_score} / 500** очков"

    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')


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

    # Проверяем момент, когда пользователь ровно дошел до 500 очков для разбана
    if current_score == 500:
        scores[user.id] = 0  # Сбрасываем баланс на 0, теперь можно тапать бесконечно дальше
        await query.edit_message_text(
            f"🎉 Поздравляем, @{user.username or user.first_name}!\n\n"
            "Ты натапал **500 очков** и получил разбан! 🔓 Твой баланс сброшен на 0. Теперь можешь тапать дальше сколько угодно, но если снова получишь бан — придется снова набивать 500!",
            parse_mode='Markdown'
        )
        return

    # Если баланс перешагнул 500 (игрок тапает бесконечно после разбана)
    if current_score > 500:
        text = f"🏆 **Твой кликер**\n\nБаланс: **{current_score}** очков (свободный режим)"
    else:
        text = f"🏆 **Твой кликер**\n\nБаланс: **{current_score} / 500** очков"

    # Обновляем текст в сообщении с новым балансом
    keyboard = [
        [InlineKeyboardButton("👆 TAP", callback_data="click_action")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')


# Главная функция запуска
if __name__ == '__main__':
    print("Бот-кликер с цикличным разбаном запускается...")
    
    application = ApplicationBuilder().token(TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('gameclicker', gameclicker_command))
    
    # Обработчик нажатий на инлайн-кнопки
    application.add_handler(CallbackQueryHandler(button_handler, pattern="click_action"))

    print("Бот работает!")
    application.run_polling()
    
