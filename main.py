
import telebot
from telebot import types
import os
import re

TOKEN = "8104879861:AAEu8DGjBeocnwQ4xkyp48GOoC0kZshwf30"
bot = telebot.TeleBot(TOKEN)

user_data = {}

STEPS = ['district', 'room', 'area', 'budget']
properties = [
    {
        "id": 123,
        "district": "Сихівський район 🌳",
        "rooms": 1,
        "area": 60,
        "budget": 1100,
        "description": "Квартира дуже чудова",
        "photos": [r"D:\\labs\\labs_2_kurs\\kurs\\photos\\photo_2024-09-30_09-54-52.jpg", "D:\\labs\\labs_2_kurs\\kurs\\photos\\photo_2024-10-03_22-07-56.jpg"]
    },
    {
        "id": 124,
        "district": "Галицький район 🏰",
        "rooms": 1,
        "area": 55,
        "budget": 800,
        "description": "Непога квартира",
        "photos": [r"D:\labs\labs_2_kurs\kurs\photos\photo_2024-10-03_22-07-56.jpg"]
    },
]


def get_prev_step(chat_id):
    current_index = STEPS.index(user_data[chat_id]['current_step'])
    return STEPS[max(0, current_index - 1)]


def extract_number(text):
    match = re.search(r'\d+', text)
    return int(match.group()) if match else None


def filter_properties(chat_id):
    filtered_properties = []
    user_selections = user_data[chat_id]
    for property in properties:
        user_rooms = extract_number(user_selections['room'])
        user_area = extract_number(user_selections['area'])
        user_budget = extract_number(user_selections['budget'])

        if (property['district'] == user_selections['district'] and
                property['rooms'] == user_rooms and
                property['area'] <= user_area and
                property['budget'] <= user_budget):
            filtered_properties.append(property)
    return filtered_properties


def send_filtered_properties(chat_id, filtered_properties):
    if not filtered_properties:
        bot.send_message(chat_id, "На жаль, за вашими критеріями нічого не знайдено. ☹️")
        return
    for property in filtered_properties:
        message = f"Опис: {property['description']}\nРайон: {property['district']}\nКімнат: {property['rooms']}\nПлоща: {property['area']}м²\nБюджет: ${property['budget']}"
        bot.send_message(chat_id, message)
        for photo in property['photos']:
            if os.path.exists(photo):
                bot.send_photo(chat_id, photo=open(photo, 'rb'))
            else:
                bot.send_message(chat_id, "[Фото недоступне]")


def handle_choice(chat_id, data, message_id):
    current_step = user_data[chat_id]['current_step']
    user_data[chat_id][current_step] = data.split('_')[1]

    next_step_index = STEPS.index(current_step) + 1
    if next_step_index < len(STEPS):
        next_step = STEPS[next_step_index]
        user_data[chat_id]['current_step'] = next_step
        bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                              text=f"Вибрано {data.split('_')[1]}. Ваш наступний вибір:",
                              reply_markup=get_keyboard(next_step))
    else:
        filtered_properties = filter_properties(chat_id)
        send_filtered_properties(chat_id, filtered_properties)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    data = call.data

    if data == 'back':
        prev_step = get_prev_step(chat_id)
        user_data[chat_id]['current_step'] = prev_step
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                              text=f"Повертаємось на крок: {prev_step}", reply_markup=get_keyboard(prev_step))
    else:
        handle_choice(chat_id, data, call.message.message_id)


@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'current_step': 'district'}
    welcome_message = ("Привіт!👋\n"
                       "Ласкаво просимо до нашого ріелторського бота!🏡\n"
                       "Ми тут, щоб допомогти Вам знайти ідеальне житло в ідеальному місті.\n"
                       "В якому районі Ви плануєте мешкати?🤔")
    bot.send_message(chat_id, welcome_message, reply_markup=create_district_keyboard())


@bot.message_handler(commands=['test'])
def handle_test(message):
    bot.send_message(message.chat.id, "Тестове повідомлення.")


def create_district_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    districts = ["Сихівський район 🌳", "Галицький район 🏰", "Залізничний район 🚉", "Франківський район 🏞️",
                 "Личаківський район 🍀", "Шевченківський район 🌆"]
    buttons = [types.InlineKeyboardButton(text=district, callback_data=f'district_{district}') for district in
               districts]
    keyboard.add(*buttons)
    return keyboard


def create_room_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    rooms = ["1-кімнатна", "2-кімнатна", "3-кімнатна", "4-кімнатна"]
    buttons = [types.InlineKeyboardButton(text=room, callback_data=f'room_{room}') for room in rooms]
    keyboard.add(*buttons)
    return keyboard


def create_area_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    areas = ["до 30 кв.м", "до 40 кв.м", "до 50 кв.м", "до 70 кв.м", "до 90 кв.м", "до 110 кв.м", "до 130 кв.м",
             "до 150 кв.м", "до 170 кв.м", "до 190 кв.м", "від 200 кв.м"]
    buttons = [types.InlineKeyboardButton(text=area, callback_data=f'area_{area}') for area in areas]
    keyboard.add(*buttons)
    return keyboard


def create_budget_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    budgets = ["до 400$", "до 500$", "до 600$", "до 700$", "до 800$", "до 900$", "до 1000$", "до 1100$",
               "до 1200$", "до 1300$", "до 1400$", "від 1400$"]
    buttons = [types.InlineKeyboardButton(text=budget, callback_data=f'budget_{budget}') for budget in budgets]
    keyboard.add(*buttons)
    return keyboard


def get_keyboard(step):
    keyboard = types.InlineKeyboardMarkup()

    if step != 'district':
        keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="back"))

    if step == 'district':
        return keyboard.add(*[types.InlineKeyboardButton(text=d, callback_data=f'district_{d}') for d in
                              ["Сихівський район 🌳", "Галицький район 🏰", "Залізничний район 🚉",
                               "Франківський район 🏞️",
                               "Личаківський район 🍀", "Шевченківський район 🌆"]])
    elif step == 'room':
        return keyboard.add(*[types.InlineKeyboardButton(text=r, callback_data=f'room_{r}') for r in
                              ["1-кімнатна", "2-кімнатна", "3-кімнатна", "4-кімнатна"]])
    elif step == 'area':
        return keyboard.add(*[types.InlineKeyboardButton(text=a, callback_data=f'area_{a}') for a in
                              ["до 30 кв.м", "до 40 кв.м", "до 50 кв.м", "до 70 кв.м", "до 90 кв.м", "до 110 кв.м",
                               "до 130 кв.м", "до 150 кв.м", "до 170 кв.м", "до 190 кв.м", "від 200 кв.м"]])
    elif step == 'budget':
        return keyboard.add(*[types.InlineKeyboardButton(text=b, callback_data=f'budget_{b}') for b in
                              ["до 400$", "до 500$", "до 600$", "до 700$", "до 800$", "до 900$", "до 1000$", "до 1100$",
                               "до 1200$", "до 1300$", "до 1400$", "від 1400$"]])

    return keyboard


if __name__ == '__main__':
    bot.polling(none_stop=True)
