import requests
from datetime import date
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def create_keyboard(response):
    keyboard = VkKeyboard()

    if response == 'привет':
        keyboard.add_button('Поиск', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Работа с избранными', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Работа с черным списком', color=VkKeyboardColor.POSITIVE)

    elif response == 'работа с избранными':
        keyboard.add_button('перенести в черный список', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Лайк/дизлайк', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Отправить сообщение', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Следующий', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Вернуться в начало', color=VkKeyboardColor.NEGATIVE)

    elif response == 'работа с черным списком':
        keyboard.add_button('Перенести в избранное', color=VkKeyboardColor.POSITIVE)
        # keyboard.add_button('Лайк/дизлайк', color=VkKeyboardColor.POSITIVE)
        # keyboard.add_button('Отправить сообщение', color=VkKeyboardColor.POSITIVE)
        # keyboard.add_button('Следующий', color=VkKeyboardColor.POSITIVE)
        # keyboard.add_button('Вернуться в начало', color=VkKeyboardColor.NEGATIVE)

    elif response == 'поиск':
        # keyboard.add_button('Добавить в избранное', color=VkKeyboardColor.POSITIVE)
        # keyboard.add_button('Добавить в черный список', color=VkKeyboardColor.POSITIVE)
        # keyboard.add_button('Лайк/дизлайк', color=VkKeyboardColor.POSITIVE)
        # keyboard.add_button('Отправить сообщение', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Следующий в поиске', color=VkKeyboardColor.POSITIVE)
        # keyboard.add_button('Вернуться в начало', color=VkKeyboardColor.NEGATIVE)

    elif response == 'следующий в поиске':
        # keyboard.add_button('Добавить в избранное', color=VkKeyboardColor.POSITIVE)
        # keyboard.add_button('Добавить в черный список', color=VkKeyboardColor.POSITIVE)
        # keyboard.add_button('Лайк/дизлайк', color=VkKeyboardColor.POSITIVE)
        # keyboard.add_button('Отправить сообщение', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Следующий в поиске', color=VkKeyboardColor.POSITIVE)
        # keyboard.add_button('Вернуться в начало', color=VkKeyboardColor.NEGATIVE)



    else:
        keyboard = None

    keyboard = keyboard.get_keyboard()
    return keyboard

class UserResultsStorage:
    def __init__(self):
        self.users = {}

    def add_user(self, user_id):
        if user_id not in self.users:
            self.users[user_id] = []

    def add_data(self, user_id, data):
        if user_id in self.users:
            self.users[user_id].append(data)
        else:
            self.add_user(user_id)
            self.users[user_id].append(data)

    def get_data(self, user_id):
        return self.users[user_id][0].pop(0)


class VkBot:
    base_url = 'https://api.vk.com/method/'
    def __init__(self, user_id, token_1, token_2, user_results):

        self.token_1 = token_1
        self.token_2 = token_2
        self._USER_ID = user_id
        # self.common_params = {"access_token": self.token, "v": "5.131"}
        self._USER_DATA = self._get_user_data_from_vk_id(user_id)
        self._COMMANDS = ["ПРИВЕТ", "ПОИСК", "СЛЕДУЮЩИЙ В ПОИСКЕ", "РАБОТА С ИЗБРАННЫМ",
                          "ДОБАВИТЬ В ИЗБРАННОЕ", "СПИСОК ИЗБРАННОГО", "ПОКА"]
        self.user_results = user_results



    @staticmethod
    def calculate_age(birth_date):
        data = [int(el) for el in birth_date.split('.')]
        if len(data) != 3:
            return 0
        today = date.today()
        age = today.year - data[2]-1 + ((today.month > data[1])
                                        or (today.month == data[1] and today.day >= data[0]))
        return age

    def _get_user_data_from_vk_id(self, user_id):
        params = {"access_token": self.token_1, "v": "5.131"}
        url = self.base_url + 'users.get?'
        params.update({
            "user_ids": user_id,
            "fields": "sex,first_name,last_name,deactivated,is_closed,bdate,books,city,interests,movies,music,relation"
        })
        response = requests.get(url, params=params)
        try:
            response = response.json()['response'][0]
        except:
            return None
        if 'bdate' in response.keys():
            response['age'] = VkBot.calculate_age(response['bdate'])
            del response['bdate']
        else:
            response['age'] = 0

        return response

    def search_boy_girl_friends(self, user_data: dict):
        url = self.base_url + 'users.search?'
        params = {"access_token": self.token_2, "v": "5.131"}
        if user_data['sex'] == 0:
            sex = 0
        elif user_data['sex'] == 1:
            sex = 2
        else:
            sex = 1
        if user_data['age'] == 0:
            min_age, max_age = 18, 30
        else:
            min_age, max_age = max(
                18, user_data['age'] - 5), max(18, user_data['age'] + 5)
        params.update({
            'city': user_data['city']['id'],
            'sex': sex,
            'age_from': min_age,
            'age_to': max_age,
            'fields': "sex,first_name,last_name,deactivated,is_closed,bdate,books,city,interests,movies,music,relation",
            'count': 1000
        })

        response = requests.get(url, params=params)
        try:
            response = response.json()["response"]
            count, items = response["count"], response["items"]
        except:
            return f"Не удалось найти пользователей для знакомств"

        self.user_results.add_user(self._USER_DATA['id'])
        self.user_results.add_data(self._USER_DATA['id'], items)



        return f"Найдены записи о {count} пользователях для знакомства. Для просмотра введите команду 'Следующий'"

    def execute_command(self, comand: str):

        # Привет
        if comand.strip().upper() == self._COMMANDS[0]:
            keyboard = create_keyboard(comand.strip().lower())
            message = f"Привет, {self._USER_DATA['first_name']}!"
            return message, keyboard

        # Поиск
        elif comand.strip().upper() == self._COMMANDS[1]:
            keyboard = create_keyboard(comand.strip().lower())
            message = self.search_boy_girl_friends(self._USER_DATA)
            return message, keyboard

        # Выдача следующего результата
        elif comand.strip().upper() == self._COMMANDS[2]:
            next_item = self.user_results.get_data(self._USER_DATA['id'])
            first_name = next_item['first_name']
            last_name = next_item['last_name']
            birth_date = next_item['bdate']
            message =  f"Имя: {first_name}\nФамилия: {last_name}\nДата рождения: {birth_date}"
            keyboard = create_keyboard(comand.strip().lower())
            return message, keyboard

        # Добавление пользователя в избранное
        elif comand.strip().upper() == self._COMMANDS[3]:
            '''Нужен код для добавления метки избранное для пользователя в БД'''
            return ' '

        # Вывести список избранного
        elif comand.strip().upper() == self._COMMANDS[4]:
            '''Нужен код для вывода списка избранного'''
            return ' '

        # Пока
        elif comand.strip().upper() == self._COMMANDS[5]:
            return f"Пока, {self._USER_DATA['first_name']}!"

        else:
            return "Не понимаю о чем вы..."
