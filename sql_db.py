import sqlite3


class SqlChatBase:

    def __init__(self, database):
        """ Подключается к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def chat_exists(self, chat_id):
        """ Проверяет, есть ли уже id чата в базе """
        with self.connection:
            result = self.cursor.execute(
                'SELECT `chat_id` FROM `chats` WHERE `chat_id` = ?', [chat_id]).fetchone()
            return result

    def message_exist(self, chat_id):
        """ Возвращает номер сообщения определенного chat_id """
        with self.connection:
            message_id = self.cursor.execute(
                'SELECT `message_id` FROM `chats` WHERE `chat_id` = ?', [chat_id]).fetchone()
            result = int(message_id[0])
            return result

    def update_call_data(self, chat_id, call_data):
        """ Обновляет call.data у определенного chat_id """
        with self.connection:
            return self.cursor.execute(
                "UPDATE `chats` SET `last_call` = '?' WHERE `chat_id` = '?'", [call_data, chat_id])

    def return_last_call(self, chat_id):
        """ Возвращает последий call.data определенного chat_id """
        with self.connection:
            last_call = self.cursor.execute(
                'SELECT `last_call` FROM `chats` WHERE `chat_id` = ?', [chat_id]).fetchone()
        result = str(last_call[0])
        return result

    def add_chat(self, chat_id, message_id):
        """ Добавляет новоый id чата """
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `chats` (`chat_id`, `message_id`) VALUES(?, ?)", [chat_id, message_id])

    def return_message_id(self, chat_id):
        """ Возвращает id сообщения """
        with self.connection:
            return self.cursor.execute(
                'SELECT `message_id` FROM `chats` WHERE `chat_id` = ?', [chat_id]).fetchone()

    def update_message_id(self, chat_id, message_id):
        """ Обновляет id сообщения """
        with self.connection:
            return self.cursor.execute(
                "UPDATE `chats` SET `message_id` = ? WHERE `chat_id` = ?", [message_id, chat_id])

    def close(self):
        """ Закрывает соединение с БД """
        self.connection.close()


class SqlParseFilms:

    def __init__(self, database):
        """ Подключается к БД и сохраняем курсор соединения """
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def add_film(self, film_title_and_year, en_title, rus_title, poster, rating, year, duration, about):
        """
        self, film_title, rus_title, poster, rating, year, duration, info
        Запись информации в БД
        :param film_title_and_year: Название фильма + год выхода
                                    (строка должна иметь следующий вид => 'Слово1+Слово2_yГод')
        :param en_title: Название фильма на английском
        :param rus_title: Название фильма на русском
        :param poster: url на изображение постера
        :param rating: Рейтинг фильма
        :param year: Год выхода
        :param duration: Продолжительность фильма
        :param about: тест «О фильме»
        """
        with self.connection:
            self.cursor.execute(
                'INSERT INTO `parse_films` (`film_title_and_year`, `en_title`, `rus_title`, `poster`, `rating`, '
                '`year`, `duration`, `about`) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', [film_title_and_year, en_title,
                                                                                 rus_title, poster, rating, year,
                                                                                 duration, about])
            self.connection.commit()

    def name_year_db(self, genre):
        """ Возвращает список фильмов (film_title_and_year, rus_title и year), исходя из выбранного жанра """
        # В версии 1.0.0 доступен лишь вывод всех фильмов
        if genre == 'f_all':
            with self.connection:
                self.cursor.execute('SELECT `film_title_and_year`, `rus_title`, `year` FROM `parse_films`')
                return self.cursor.fetchall()

    def check_film_db(self, film_title_and_year):
        """ Запись жанра фильма """
        with self.connection:
            self.cursor.execute(
                "SELECT `en_title` FROM `parse_films` WHERE `film_title_and_year` = ?", [film_title_and_year])
        result = self.cursor.fetchone()
        if not result:
            return True
        else:
            return

    def get_film_info(self, film_title_and_year):
        """ Возвращает всю информацию о фильме """
        with self.connection:
            self.cursor.execute(
                "SELECT * FROM `parse_films` WHERE `film_title_and_year` = ?", [film_title_and_year])
        return self.cursor.fetchone()

    def get_all_t_and_y(self):
        """ Возвращает все фильмы (film_title_and_year), записанные в БД """
        with self.connection:
            self.cursor.execute('SELECT `film_title_and_year` FROM `parse_films`')
        result = self.cursor.fetchall()
        t_and_y_list = []
        for raw in result:
            t_and_y_list.append(raw[0])
        return t_and_y_list

    def close(self):
        """Закрывает соединение с БД"""
        self.connection.close()
