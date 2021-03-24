import telebot as tb
import buttons as btns
from sql_db import SqlChatBase, SqlParseFilms

DB_CHATS = SqlChatBase('db_bot.db')
DB_FILMS = SqlParseFilms('db_bot.db')
FILMS_ALL = DB_FILMS.get_all_t_and_y()
TOKEN = ''
BOT = tb.TeleBot(token=TOKEN)
print(BOT.get_me())


def ms_film_page(callback_data, calling):
    """ Создает информативную страницу с фильмом """
    film_info = DB_FILMS.get_film_info(callback_data)
    text_film = '{} ({})\n\n    {}\n\n    Рейтинг: {}\n    {}мин'.format(film_info[2], film_info[5], film_info[7],
                                                                         film_info[4], film_info[6])
    text_film = text_film + '[.]' + '(' + film_info[3] + ')'
    last_call = DB_CHATS.return_last_call(chat_id=calling)
    button_back = btns.back_button(last_call=last_call)
    BOT.edit_message_text(text_film, chat_id=calling, message_id=DB_CHATS.message_exist(chat_id=calling),
                          parse_mode='markdown', reply_markup=button_back)


def genres_lists(calling, text='Text', buttons=btns.MAIN_MENU):
    """ Вывод текста и списка кнопок с заменой предыдущего сообщения """
    BOT.edit_message_text(text, chat_id=calling, message_id=DB_CHATS.message_exist(chat_id=calling),
                          reply_markup=buttons)


@BOT.message_handler(commands=['start'])
def send_welcome(message):
    """ Приветственное сообщение, также обновляет номер сообщения в БД у пользователя """
    msg_new = BOT.send_message(message.chat.id, "Привет, я создан для помощи в поиске чего-нибудь интересного\n\nДля "
                                                "выбора категории просто жми «Категории»",
                               reply_markup=btns.GO_LIST)
    chat_id = message.chat.id
    if not DB_CHATS.chat_exists(chat_id):
        DB_CHATS.add_chat(chat_id=chat_id, message_id=msg_new.message_id)
    else:
        DB_CHATS.update_message_id(chat_id=chat_id, message_id=msg_new.message_id)


@BOT.callback_query_handler(func=lambda call: True)
def check_list(call):
    """ Вызов функций при нажатии на кнопки """
    if call.data == 'group_list':
        genres_lists(calling=call.message.chat.id, text='Выберите категорию', buttons=btns.CATEGORIES)
    elif call.data == 'films':
        genres_lists(calling=call.message.chat.id, text='Выберите жанр фильма', buttons=btns.FILM_GENRES)
    elif call.data[0:2] == 'f_':
        DB_CHATS.update_last_call(chat_id=call.message.chat.id, call_data=call.data)
        if call.data == 'f_all':
            films_buttons = btns.create_inline_buttons(db=DB_FILMS, genre=call.data)
            genres_lists(calling=call.message.chat.id, text='Все фильмы:', buttons=films_buttons)
        else:
            pass
    elif call.data in FILMS_ALL:
        ms_film_page(callback_data=call.data, calling=call.message.chat.id)


if __name__ == '__main__':
    BOT.polling(none_stop=False, interval=0, timeout=20)
