import sqlite3
import time

import telebot
from telebot import types

import markups as mark
import quests as qst
import specialists as spec
from config import token_api
from intro_text import intro_text

my_id = "786254617" # Ваш айди куда будет приходить сообщения с информацией о юзере и его заявке

def get_info_user(bot, message, admin):  # ФУНКЦИЯ ОБ ОТПРАВКИ СООБЩЕНИЯ
          if admin:
              #для отправки жалобы
              bot.send_message(my_id, 'Менеджер вам послание об жалобе!!😮\n'+ message.text
                              + ' '
                              + f'{message.from_user.first_name}' + ' '
                              + f'{message.from_user.last_name}'+ ' username @'
                              f'{message.from_user.username}')
          else:
              #для отправки сообщения спецалисту
              bot.send_message(spec.ids[spec.act_id], spec.names[spec.act_id] +'! Вам сообщение:\n'+  message.text + ' '
                              + ' '
                              + f'{message.from_user.first_name}' + ' '
                              + f'{message.from_user.last_name}'+ ' username @'
                              f'{message.from_user.username}')


      #запуск бота
def run_bot():
          id_spec=0
          bot = telebot.TeleBot(token_api)

          @bot.message_handler(commands=['start'])  # приветственная функция
          def send_welcome(message):
              conn = sqlite3.connect('users_manager_bot.db') #подключение к базе данных
              cur = conn.cursor()
              cur.execute("""CREATE TABLE IF NOT EXISTS users(
                  userid INT PRIMARY KEY,
                  fname TEXT,
                  lname TEXT);
              """)
              conn.commit() #для сохранения о том кто вошел в бота

              user_info = (f'{message.chat.id}',
                          f'{message.from_user.first_name}',
                          f'{message.from_user.last_name}'
                          f'{message.from_user.username}')

              cur.execute("INSERT OR IGNORE INTO users VALUES(?, ?, ?);", user_info)  
              conn.commit() #добавление в таблицу инфа о пользователе 

              img = open('title.jpg', 'rb')
              bot.send_photo(message.chat.id, img)#отправка картинки
              welcome_user = f'Здравствуйте😊 {message.from_user.first_name} {message.from_user.last_name}' + intro_text   
              bot.send_message(message.chat.id, welcome_user, reply_markup=mark.main_menu)

          @bot.message_handler(content_types=['text'])
          def send_markup(message):
              if message.text == 'Жалоба':
                  bot.send_message(message.chat.id, 'Хорошо😥! Опишите свою проблему'
                                                  ' и в конце своего описания поставьте символ @ '
                                                  '\nчто-бы я поняла Вас. Наш менеджер в ближайшее время сам вам напишет!', reply_markup=mark.del_markup)
              elif '@' in message.text:
                  bot.send_message(message.chat.id, 'Спасибо, с Вами свяжутся в ближайшее время!😉',
                                   reply_markup=mark.any_func)
                  get_info_user(bot, message, True)

              elif message.text == 'Cпециалисты':
                          bot.send_message(message.chat.id, 'Хорошо! Выберите специалиста!🙂',
                                           reply_markup=mark.specs)
                #показ специалистов

              elif message.text == 'Светлана':
                        spec.act_id=0
                        bot.send_message(message.chat.id, f'Вы выбрали Светлану! Стаж работы:{spec.staj[spec.act_id]} года/лет. Профиль: {spec.tag[spec.act_id]}. '
                                                            'Хотите связаться?',
                                           reply_markup=mark.call_specs)
              elif message.text == 'Татьяна':
                        spec.act_id=1
                        bot.send_message(message.chat.id, f'Вы выбрали Татьяну! Стаж работы:{spec.staj[spec.act_id]} года/лет. Профиль: {spec.tag[spec.act_id]}. '
                                           'Хотите связаться?',
                                         reply_markup=mark.call_specs)
              elif message.text == 'Маргарита':
                        spec.act_id=2
                        bot.send_message(message.chat.id, f'Вы выбрали Маргариту! Стаж работы:{spec.staj[spec.act_id]} года/лет. Профиль: {spec.tag[spec.act_id]}. '
              'Хотите связаться?',
                                           reply_markup=mark.call_specs)
              elif message.text == 'Луиза':
                        spec.act_id=3
                        bot.send_message(message.chat.id, f'Вы выбрали Луизу! Стаж работы:{spec.staj[spec.act_id]} года/лет. Профиль: {spec.tag[spec.act_id]}. '
                                           'Хотите связаться?',
                                           reply_markup=mark.call_specs)
              elif message.text == 'Карина':
                        spec.act_id=4
                        bot.send_message(message.chat.id, f'Вы выбрали Карину! Стаж работы:{spec.staj[spec.act_id]} года/лет. Профиль: {spec.tag[id_spec]}. '
                                           'Хотите связаться?',
                                     reply_markup=mark.call_specs)

              elif message.text == 'Связаться':
                        bot.send_message(message.chat.id, 'Хорошо😊! Напишите сообщение для начала диалога со специалистом'
                          ' и в конце своего описания поставьте символ * '
                          '\nчто-бы я поняла Вас. Ваш специалист в ближайшее время сам вам напишет!😁', reply_markup=mark.del_markup)
              elif '*' in message.text:
                        bot.send_message(message.chat.id, 'Спасибо, с Вами свяжутся в ближайшее время!😉',
                        reply_markup=mark.any_func)
                        get_info_user(bot, message, False)


              # выбор вопросов с помощью Inline-кнопок
              elif message.text == 'Вопросы':
                    if message.text == 'Вопросы':
                      keyboard = types.InlineKeyboardMarkup()
                      for idx, question in enumerate(qst.questions, start=1):
                        callback_button = types.InlineKeyboardButton(text=qst.questions[idx-1], callback_data=f'question_{idx}')
                        keyboard.add(callback_button)
                      bot.send_message(message.chat.id, qst.text_quest, reply_markup=keyboard)

              elif message.text == 'О компании':
                    bot.send_message(message.chat.id, '🌷🌸Салон красоты "Под Феном"🌼🌻 - это уютное пространство, где каждая стрижка превращается в настоящее творчество. Наши опытные стилисты работают с любовью к деталям и стремятся создать идеальный образ для каждого клиента. Здесь вы не просто обретете новую прическу, а откроете для себя новый уровень ухода за волосами и стиля.\n  😊Доверьтесь нам, и вы уйдете от нас не только с прекрасным результатом, но и с незабываемым опытом, который заставит вас возвращаться к нам снова и снова. \n 😉Добро пожаловать в парикмахерскую "Под Феном" - где ваш образ превращается в искусство! \n Баклановский 105а.торговый центр Поиск\n👩‍🦰Окрашевания любой сложности. \nСтрижки женские-мужские👨👩\nУкладка волос.👱‍♀️\nУход и лечение волос.👸\n89281963013\n89281793282',
                     reply_markup=mark.any_func)
              elif message.text == 'Назад':
                img = open('title.jpg', 'rb')
                bot.send_photo(message.chat.id, img)
                bot.send_message(message.chat.id, intro_text,
                               reply_markup=mark.main_menu)
              else:
                  bot.send_message(message.chat.id, 'Я Вас не поняла =(')

          # Обработчик Inline-кнопок перед запуском бота
          @bot.callback_query_handler(func=lambda call: call.data.startswith('question_'))
          def handle_question_callback(call):
              question_index = int(call.data.split('_')[1]) - 1
              bot.send_message(call.message.chat.id, qst.questions[question_index],
                               reply_markup=mark.how_ques)
              bot.send_message(call.message.chat.id, qst.answers[question_index])

          while True:  # функция для пулинга
              print('Маша успешно начала пить утренний кофе ') # информация о статусе бота в кмдной строке 

              try:
                  bot.polling(none_stop=True, interval=3, timeout=20)
                  print('Этого не должно быть')
              except telebot.apihelper.ApiException:
                  print('Проверьте связь и API')
                  time.sleep(10)
              except Exception as e:
                print(e)
                time.sleep(60)

if __name__ == '__main__':
        run_bot()