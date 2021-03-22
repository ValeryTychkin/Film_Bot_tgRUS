from telebot import types


def create_inline_buttons(db, genre):
    """
    Создает список из кнопок с названием фильмов
    :param db: База данных, откуда брать информацию для кнопок
    :param genre: Жанр фильмов
                  (на данныйй момент нельзя вывести определенный жанр, только весь список фильмов)
    :return: Список кнопок
    """
    list_buttons = types.InlineKeyboardMarkup(row_width=1)
    if genre == 'f_all':
        titles_list_db = db.name_year_db(genre)
        for title in titles_list_db:
            list_buttons.add(types.InlineKeyboardButton(callback_data=title[0], text=(title[1]+' ('+str(title[2])+')')))
        list_buttons.add(MAIN_MENU)
        return list_buttons


def back_button(last_call):
    """
    Создает кнопку, которая возвращает на предыдущий запрос
    :param last_call: Последний запрос
    :return: Кнопку
    """
    return_back = types.InlineKeyboardButton(callback_data=last_call, text='👈🏻 вернуться назад')
    return_back_button = types.InlineKeyboardMarkup(row_width=1)
    return_back_button.add(return_back, MAIN_MENU)
    return return_back_button


MAIN_MENU = types.InlineKeyboardButton(callback_data='group_list', text='❌️главное меню❌')

GROUP_LIST = types.InlineKeyboardButton(callback_data='group_list', text='Категории')
GO_LIST = types.InlineKeyboardMarkup()
GO_LIST.add(GROUP_LIST)


FILMS = types.InlineKeyboardButton(callback_data='films', text='Фильмы')
CATEGORIES = types.InlineKeyboardMarkup()
CATEGORIES.add(FILMS)

F_ALL = types.InlineKeyboardButton(callback_data='f_all', text='Все')
FILM_GENRES = types.InlineKeyboardMarkup(row_width=1)
FILM_GENRES.add(F_ALL, MAIN_MENU)
