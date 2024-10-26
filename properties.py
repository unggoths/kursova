import re

STEPS = ['district', 'room', 'area', 'budget']
properties = [
    {
        "id": 123,
        "district": "Сихівський район 🌳",
        "rooms": 1,
        "area": 60,
        "budget": 1100,
        "description": "Квартира дуже чудова",
        "phone_number": "+380 97 456 12 34",
        "photos": [r"D:\\labs\\labs_2_kurs\\kurs\\photos\\photo_2024-09-30_09-54-52.jpg",
                   r"D:\\labs\\labs_2_kurs\\kurs\\photos\\photo_2024-10-03_22-07-56.jpg"]
    },
    {
        "id": 124,
        "district": "Галицький район 🏰",
        "rooms": 1,
        "area": 55,
        "budget": 800,
        "phone_number": "+380 97 456 12 34",
        "description": "Непога квартира",
        "photos": [r"D:\labs\labs_2_kurs\kurs\photos\photo_2024-10-02_16-46-48.jpg",
                   r"D:\labs\labs_2_kurs\kurs\photos\photo_2024-10-02_16-46-48 (2).jpg",
                   r"D:\labs\labs_2_kurs\kurs\photos\photo_2024-10-02_16-46-48 (3).jpg"]
    },
]


def extract_number(text):
    match = re.search(r'\d+', text)
    return int(match.group()) if match else None


def filter_properties(chat_id, user_data):
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
