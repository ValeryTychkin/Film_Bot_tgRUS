import requests
from bs4 import BeautifulSoup
from sql_db import SqlParseFilms

DB_FILMS = SqlParseFilms('db_bot.db')
URL_KINOPOISK = 'http://kinopoisk.ru'
URL_KINOPOISK_SEARCH = '/index.php?kp_query='
URL_FILMZ = 'https://filmz.ru'
URL_FILMZ_SEARCH_FIRST = '/search/?search='
URL_FILMZ_SEARCH_SECOND = '&where_search=all'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko)'
                  'Chrome/85.0.4183.121 Safari/537.36',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
    }
TITLE_FILMS_LIST = ['Pulp+Fiction', 'American+Beauty']  # Название должно иметь следующий вид => 'Слово_1+Слово_2'


def start_parse():
    """ Запускает парсинг сайтов для сбора информации о фильме и записывает ее в БД """
    for title in TITLE_FILMS_LIST:
        url_film = film_page(title)
        year = film_year(url_film)
        if DB_FILMS.check_film_db(film_title_and_year=(title + '_y' + year)):  # Проверка, есть ли уже в БД данный фильм
            print(title, True)              # Если данный фильм отсутствует в БД, то выводится «"Н-азвание фильма" True»
            rating = film_rating(get_url(search_title=title, web_site='kinopoisk'))
            DB_FILMS.add_film(film_title_and_year=(title + '_y' + year), en_title=en_title(url_film),
                              rus_title=rus_title(url_film), poster=film_poster(url_film), rating=rating,
                              year=film_year(url_film), duration=film_duration(url_film), about=film_about(url_film))
        else:
            print(title, False)


def get_url(search_title, url_view='search', web_site='filmz'):
    """
    Создает url ссылку на поиск данного фильма или его страницу
    :param search_title: Название фильма
    :param url_view: 'search' = необходимо url поискового запроса фильма
                     'page'   = необходимо url страницы с фильмом
                     (если необходим 'page', то search_title это ссылка на страницу без домменого имени)
    :param web_site: выбор сайта для которого создается url
    :return: возвращает созданный url
    """
    url = None
    if web_site == 'filmz':
        if url_view == 'search':
            url = URL_FILMZ + URL_FILMZ_SEARCH_FIRST + search_title + URL_FILMZ_SEARCH_SECOND
        elif url_view == 'page':
            url = URL_FILMZ + search_title
    elif web_site == 'kinopoisk':
        if url_view == 'search':
            url = URL_KINOPOISK + URL_KINOPOISK_SEARCH + search_title
        elif url_view == 'page':
            url = URL_KINOPOISK + search_title
    if url:
        return requests.get(url=url, headers=HEADERS)
    else:
        return print('Error')


def film_page(title):
    """
    url ссылка на страницу с фильмом в filmz
    :param title: Название фильма
    :return: url на фильм
    """
    url_search = get_url(search_title=title)
    if url_search.status_code == 200:
        soup = BeautifulSoup(url_search.text, 'html.parser')
        url_film_page = soup.find('div', class_='content br5').find_next('div', class_='content br5').find('h2').find(
            'a').get('href')
        return get_url(search_title=url_film_page, url_view='page')
    else:
        print('Error')


def film_about(html_page):
    """
    Находит текст «О фильме»
    :param html_page: url на страницу фильма
    :return: текст «О фильме»
    """
    soup = BeautifulSoup(html_page.text, 'html.parser')
    return soup.find('p', class_='fs16').find_next('p', class_='fs16').string


def rus_title(html_page):
    """
    Узнает название фильма на русском
    :param html_page: url на страницу фильма
    :return: название фильма на русском
    """
    soup = BeautifulSoup(html_page.text, 'html.parser')
    return soup.find('span', itemprop='name').string


def en_title(html_page):
    """
    Узнает название фильма на английском
    :param html_page: url на страницу фильма
    :return: название фильма на английском
    """
    soup = BeautifulSoup(html_page.text, 'html.parser')
    return soup.find('span', itemprop='alternativeHeadline').string


def film_year(html_page):
    """
    Узнает, в каком году вышел фильм
    :param html_page: url на страницу фильма
    :return: год выхода фильма
    """
    soup = BeautifulSoup(html_page.text, 'html.parser')
    return soup.find('span', itemprop='dateCreated').string


def film_duration(html_page):
    """
    Узнает продолжительность фильма
    :param html_page: url на страницу фильма
    :return: продолжительность фильма
    """
    soup = BeautifulSoup(html_page.text, 'html.parser')
    return soup.find('span', itemprop='duration').string


def film_poster(html_page):
    """
    Находит постер фильма
    :param html_page: url на страницу фильма
    :return: url на постер фильма
    """
    soup = BeautifulSoup(html_page.text, 'html.parser')
    poster_page_url = soup.find('li', class_='first active').find_next('li').find_next('li').find_next('li').find_next(
        'li').find('a').get('href')
    poster_page_url = URL_FILMZ + poster_page_url
    poster_page = requests.get(url=poster_page_url, headers=HEADERS)
    soup = BeautifulSoup(poster_page.text, 'html.parser')
    poster_page_url = soup.find('a', class_='fullink').find_next('a').get('href')
    poster_page = requests.get(url=(URL_FILMZ + poster_page_url), headers=HEADERS)
    soup = BeautifulSoup(poster_page.text, 'html.parser')
    return soup.find('img', itemprop='contentURL').get('src')


def film_rating(html_page):
    """
    Узнает оценку фильма
    :param html_page: url на страницу фильма
    :return: Оценка фильма
    """
    soup = BeautifulSoup(html_page.text, 'html.parser')
    return soup.find('div', class_='right').find_next('div').string


if __name__ == '__main__':
    start_parse()
