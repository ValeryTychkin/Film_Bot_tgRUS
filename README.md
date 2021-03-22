# Film_Bot_tgRUS  
  
**Version 1.0.0**  
  
Телеграм бот, в задачи которого входит вывод списка фильмов. Необходимо написать название фильмов, а всю информацию о фильме бот соберет за вас.  
  ___
## How to Start  
>Библиотеки: «telebot», «sqlite3», «bs4.BeautifulSoup».

#### Добавление Фильмов:  
  
__Для добавления в БД информации о фильмах необходимо запустить парсинг.__  

1. В списке «__TITLE_FILMS_LIST__» (находящемся в файле «___parse_films_func.py___») вписать название фильмов.  
![titles_films](https://psv4.userapi.com/c534536/u49035380/docs/d36/44119972c975/Snimok_ekrana_2021-03-22_v_12_15_51.png?extra=nkYiha4Q9euB6Rjlys-nWBde4yxfRbQpuaIsrCzv7F_6ZadOhMrVYuDXSJOF7m7K0oWbkAQZ4FGqTkUZCqMLQruU1LwS3q6TprRFQxx91wcxfanUMFny2PbJvh4uI1XbVpqucbTEPuefxS5-BQA5TDk)  
   >крайне желательно вписывать английские названия фильмов  

  2. После добавления названия фильмов можно запускать данный файл «___parse_films_func.py___».  
  Вся необходимая информация будет записана в таблицу «__parse_films__» (находящемся в файле «___db_bot.db___»)
#### Запуск Бота:  
__Для запуска бота необходимо:__  

1. Вписать токен вашего бота в глобальную переменную «__TOKEN__» (находящуюся в файле «___main.py___») 
![token](https://psv4.userapi.com/c536436/u49035380/docs/d29/5ab8959b28ac/Snimok_ekrana_2021-03-22_v_13_37_48.png?extra=mPwWezqCJc9fyy8cEYapFMjndy7tF7t8nXzdPxYcwZvpFFtxDGxD5g-us7QYQ2n71C6m224ZDMoElT77LPCjpOYMJWtnjL-Pc3cfQ0l5vtya-R6IysAKmSCYqM6PruEfQ8zTrOPd93X0vIgG3SF2jAw) 
2. Запустить файл «___main.py___»
  ___
## Контакты для Связи
- __Email__: [valery.tychkin@gmail.com](valery.tychkin@gmail.com)  
- [Telegram](https://t.me/ILove1337)
