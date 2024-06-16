import telebot
import requests
from datetime import datetime
from telebot import types

# Токен вашего бота, полученный от @BotFather
API_TOKEN = 'token'

# Список криптовалют для отслеживания (можно добавить или изменить по вашему усмотрению)
crypto_currencies = [
    {'name': 'Notcoin', 'symbol': 'NOT'},
    {'name': 'KAKAXA', 'symbol': 'KAKAXA'},
    {'name': 'the-open-network', 'symbol': 'TON'},
    {'name': 'TRON', 'symbol': 'TRX'},
]

# Функция для получения текущего курса криптовалюты
def get_crypto_prices():
    prices = {}
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': ','.join([crypto['name'].lower().replace(' ', '-') for crypto in crypto_currencies]),
        'vs_currencies': 'usd'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        for crypto in crypto_currencies:
            name = crypto['name']
            symbol = crypto['symbol']
            if name.lower().replace(' ', '-') in data:
                prices[name] = data[name.lower().replace(' ', '-')]['usd']
    return prices
def get_crypto_pricess():
    pricess = {}
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': ','.join([crypto['name'].lower().replace(' ', '-') for crypto in crypto_currencies]),
        'vs_currencies': 'rub'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        for crypto in crypto_currencies:
            name = crypto['name']
            symbol = crypto['symbol']
            if name.lower().replace(' ', '-') in data:
                pricess[name] = data[name.lower().replace(' ', '-')]['rub']
    return pricess

# Создаем экземпляр бота
bot = telebot.TeleBot(API_TOKEN)

# Обработчик команды /kurs
@bot.message_handler(commands=['kurs'])
def send_crypto_prices(message):
    # Получаем текущие курсы криптовалют
    prices = get_crypto_prices()
    pricess = get_crypto_pricess()
    
    # Формируем текст для отправки
    text = "<b>Курсы криптовалют:</b>\n"
    for crypto in crypto_currencies:
        name = crypto['name']
        symbol = crypto['symbol']
        if name in prices:
            text += f"{symbol}: ${prices[name]:,.5f} | ₽{pricess[name]:,.5f}\n"
        else:
            text += f"{symbol}: Нет данных\n"
    
    # Создаем клавиатуру с кнопкой "Обновить курс"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Обновить курс"))
    
    # Отправляем сообщение с курсами и клавиатурой
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=keyboard)

# Обработчик нажатия на кнопку "Обновить курс"
@bot.message_handler(func=lambda message: message.text == 'Обновить курс')
def refresh_prices(message):
    # Получаем и отправляем обновленные курсы
    prices = get_crypto_prices()
    text = "<b>Обновленные курсы криптовалют:</b>\n"
    for crypto in crypto_currencies:
        name = crypto['name']
        symbol = crypto['symbol']
        if name in prices:
            text += f"{symbol}: ${prices[name]:,.5f} | ₽{pricess[name]:,.5f}\n"
        else:
            text += f"{symbol}: Нет данных\n"
    
    bot.send_message(message.chat.id, text, parse_mode='HTML')

# Запускаем бота
if __name__ == '__main__':
    bot.polling(none_stop=True)