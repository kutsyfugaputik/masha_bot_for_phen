import telebot

# --- Main menu ---
main_menu = telebot.types.ReplyKeyboardMarkup(True)
main_menu.row('Жалоба', 'Cпециалисты', 'Вопросы')

# ---specialist menu ---
specs = telebot.types.ReplyKeyboardMarkup(True)
specs.row('Светлана','Татьяна','Маргарита','Луиза','Карина','Назад')
call_specs = telebot.types.ReplyKeyboardMarkup(True)
call_specs.row('Связаться','Назад')
# --- Delete markup ---
del_markup = telebot.types.ReplyKeyboardRemove()

# --- questions ---
how_ques = telebot.types.ReplyKeyboardMarkup(row_width=1)
how_ques.add('Вопросы', 'О компании','Назад')

# --- any function ---
any_func = telebot.types.ReplyKeyboardMarkup(True)
any_func.row('Назад')