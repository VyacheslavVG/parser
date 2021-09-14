from aiogram import types , executor , Dispatcher ,Bot
from config import TOKEN
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton , InlineKeyboardMarkup
import sqlite3
bot = Bot(token=TOKEN)

class OrderSettingsBot(StatesGroup):
    waiting_for_key_word = State()
    waiting_for_time = State()

dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def begin(message: types.Message):
    markup = InlineKeyboardMarkup()
    btn_1 = InlineKeyboardButton('Тест',callback_data='btn_1')
    markup.add(btn_1)
    await bot.send_message(message.chat.id, 'Бот создан для помощи фрилансерам в поиске заказов . Для использования бота в тестовом режиме необходимо нажать кнопку тест . После этого по истечению 7 дней , вам будет предложенно купить подписку стоимость 100  рублей без ограничени по времени.', reply_markup=markup)
@dp.callback_query_handler(text="btn_1")
async def send_answer_btn_1(call: types.CallbackQuery):
    await call.message.answer('Настройка бота ! \nНапишите ключевое слово по которому будет осуществляться поиск объявлений.')
    await OrderSettingsBot.waiting_for_key_word.set()

async def key_word(message: types.Message, state: FSMContext):
    await state.update_data(key_word=message.text.lower())
    await OrderSettingsBot.next()
    await message.answer('Выберите время в которое вам присылать рассылку в формате чч:мм')


# conn = sqlite3.connect('../bd.db')  # ПОДКЛЮЧЕНИЕ К БД
# cur = conn.cursor()
# conn.commit()
# cur.execute("INSERT INTO users(id, time) VALUES(?, ?)",el)  # доБАВЛЯЕМ ДАННЫЕ В ТАЬЛИЦУ бд
# conn.commit()")  # КОД ДЛЯ СОЗДАНИЯ ТАБЛИЦЫ БАЗЫ ДАННЫХ
# conn.commit()
executor.start_polling(dp)
