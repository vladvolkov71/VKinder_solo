import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from vk_bot import VkBot
from vk_bot import UserResultsStorage

import configparser


def get_tokens(file_name: str = "config.ini"):
    config = configparser.ConfigParser()
    config.read(file_name)
    group_token = config['VK']['group_token']
    personal_token = config['VK']['personal_token']
    return group_token, personal_token


def start_vk_bot(token_1, token_2):
    vk = vk_api.VkApi(token=token_1)
    longpoll = VkLongPoll(vk)



    def write_msg(user_id, mess, keyboard=None):
        if keyboard is not None:
            vk.method('messages.send', {
            'user_id': user_id, 'message': mess, 'random_id': randrange(10 ** 7), 'keyboard': keyboard})
        else:
            vk.method('messages.send', {
                'user_id': user_id, 'message': mess, 'random_id': randrange(10 ** 7)})

    user_results = UserResultsStorage()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                bot = VkBot(event.user_id, token_1, token_2, user_results)
                message, keyboard = bot.execute_command(event.text)
                write_msg(event.user_id, message, keyboard)



if __name__ == "__main__":
    tok_1, tok_2 = get_tokens()
    start_vk_bot(tok_1, tok_2)
