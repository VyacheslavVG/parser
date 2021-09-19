from aiogram import types , executor , Dispatcher ,Bot
from config import TOKEN
import logging
from aiogram.types import InlineKeyboardButton , InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3

available_time =['09:00','12:00','15:00','18:00','21:00','00:00','Готово']

class EnterTheData(StatesGroup):
    enter_the_keyword = State()
    enter_the_time = State()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
data = {'id':None , 'key_word': None,'t1':False,'t2':False,'t3':False,'t4':False,'t5':False,'t6':False}
@dp.message_handler(commands='start')
async def start(message: types.Message) :
    markup = InlineKeyboardMarkup()
    btn_1 = InlineKeyboardButton('Далее', callback_data='btn_1')
    markup.add(btn_1)
    await bot.send_message(message.chat.id, 'Этот бот создан для помощи фрилансерам в поисках заказов.Нажмите кнопку далее чтобы использовать бота.', reply_markup=markup)

@dp.callback_query_handler(text='btn_1')
async def next(message: types.Message):
    id = message.from_user.id
    print(id)
    # if(not db.subscriber_exists(message.from_user.id)):
    #     db.add_subscriber(message.from_user.id)
    # else:
    #     db.update_subscription(message.from_user.id, True)
    await bot.send_message(message.from_user.id,'Введите ключевое слво по которому будет осуществляться поиск заказов.')
    await EnterTheData.enter_the_keyword.set()
    data['id'] = id
@dp.message_handler(state=EnterTheData.enter_the_keyword)
async def key_word(message: types.Message, state: FSMContext):
    answer = message.text
    print(answer)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_time:
        keyboard.add(name)
    await state.update_data(answer1=answer)
    await message.answer('Выберите время в которое присылать рассылку.',reply_markup=keyboard)
    await EnterTheData.enter_the_time.set()
    data['key_word'] = answer
@dp.message_handler(state=EnterTheData.enter_the_time)
async def time(message: types.Message, state: FSMContext):
    time = message.text
    print(time)
    await state.update_data(time1=time)
    if time == '09:00' :
        data['t1'] = True
    elif time == '12:00' :
        data['t2'] = True
    elif time == '15:00' :
        data['t3'] = True
    elif time == '18:00' :
        data['t4'] = True
    elif time == '21:00' :
        data['t5'] = True
    elif time == '00:00' :
        data['t6'] = True
        print(data)
    # conn = sqlite3.connect('bd.db')  # ПОДКЛЮЧЕНИЕ К БД
    # cur = conn.cursor()
    # conn.commit()
    # cur.execute("INSERT INTO subscriptions(user_id, key_word, '09:00' , '12:00', '15:00', '18:00' , '21:00', '00:00') VALUES(:id, :key_word, :09_00 , :12_00 , :15_00, :18_00, :21_00, :00_00)",data)  # доБАВЛЯЕМ ДАННЫЕ В ТАЬЛИЦУ бд
    # conn.commit()
    if message.text == 'Готово':
        await message.answer('вы успешно подписаны')
        conn = sqlite3.connect('bd.db')  # ПОДКЛЮЧЕНИЕ К БД
        cur = conn.cursor()
        conn.commit()
        cur.execute(
            "INSERT INTO subscriptions(user_id, key_word, t0900 , t1200, t1500, t1800 , t2100, t0000) VALUES(:id, :key_word, :t1 , :t2 , :t3, :t4, :t5, :t6)",
            data)  # доБАВЛЯЕМ ДАННЫЕ В ТАЬЛИЦУ бд
        conn.commit()
        print(data)

        await state.finish()

conn = sqlite3.connect("bd.db")
c = conn.cursor()
c.execute("SELECT * FROM subscriptions ")
massive = c.fetchall()
print (massive)
executor.start_polling(dp)