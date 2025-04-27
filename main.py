import os
from dotenv import load_dotenv
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import random

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN") 

INFO_FILE = "addictive_info.txt"


class Informator:
	def __init__(self, info_file):
		self.__info_file = info_file
		self.__advices = list()
		with open(info_file, "r") as f:
			self.__advices = f.readlines()
		self.__getting_advice = False

	def get_random_advice(self) -> str:
		return random.choice(self.__advices)

	def add_advice(self, advice: str) -> None:
		if advice:
			self.__advices.append(advice.replace("\n", " "))
		with open(self.__info_file, "w") as f:
			f.write("\n".join(self.__advices))

	def is_getting_advice(self) -> bool:
		return self.__getting_advice

	def state_getting_advice_turn(self) -> None:
		self.__getting_advice = not self.__getting_advice


informator = Informator(INFO_FILE)

answers = [
	"совет такой се... ну ниче пойдет",
	"хорошо, передам.",
	"буду использовать, спасибо!",
	"фу кринж",
	"пон",
	"ОГО... Не знал"
]

information = '''
    Чтобы повысить свою продуктивность и эффективность, попробуйте следовать этим советам:

        1. Составьте список дел на день. Это поможет вам организовать своё время и сосредоточиться на выполнении задач.
        2. Установите приоритеты для каждой задачи. Определите, какие дела являются наиболее важными и требуют большего внимания.
        3. Используйте техники тайм-менеджмента, такие как метод «Помидора» или метод «АБВГД». Эти методы помогут распределить ваше время более эффективно.
        4. Делайте перерывы между задачами. Это позволит вашему мозгу отдохнуть и восстановиться перед следующей задачей.
        5. Избегайте многозадачности, так как это может привести к снижению качества работы и увеличению времени выполнения задач.
        6. Старайтесь работать в тихом месте без отвлекающих факторов (телефон, социальные сети).
        7. Выполняйте самые сложные задачи утром, когда ваша энергия находится на пике.
        8. Постоянно улучшайте свои навыки и знания в своей области деятельности.
        9. Награждайте себя за выполнение поставленных целей и достижение результатов.
        10. Наконец, не забывайте о здоровом образе жизни: правильном питании, достаточном количестве сна и физической активности.
    '''


def display_error_text(chat_id):
	markup = ReplyKeyboardMarkup(resize_keyboard=True)
	markup.add(KeyboardButton('Назад'))
	bot.send_message(chat_id, "bot don't understand что вам нужно((", reply_markup=markup)


def display_advice_answer(chat_id):
	markup = ReplyKeyboardMarkup(resize_keyboard=True)
	markup.add(KeyboardButton('Назад'))
	bot.send_message(chat_id, random.choice(answers), reply_markup=markup)


def display_information(chat_id):
	markup = ReplyKeyboardMarkup(resize_keyboard=True)
	markup.add(KeyboardButton('Назад'))
	bot.send_message(chat_id, information, reply_markup=markup)


def display_main_menu(chat_id):
	markup = ReplyKeyboardMarkup(resize_keyboard=True)
	markup.add(
		KeyboardButton('Выйти'),
		KeyboardButton('Полезная информация'),
		KeyboardButton('Обратная связь'),
		KeyboardButton('Получить случайный совет от пользователя')
	)
	bot.send_message(chat_id, 'Используйте кнопки! пж', reply_markup=markup)


def display_goodbye(chat_id):
	markup = ReplyKeyboardMarkup(resize_keyboard=True)
	markup.add(KeyboardButton('/start'))
	bot.send_message(chat_id, "Всего хорошего! и вам", reply_markup=markup)


def display_set_advice_menu(chat_id):
	markup = ReplyKeyboardMarkup(resize_keyboard=True)
	markup.add(KeyboardButton('Назад'))
	bot.send_message(chat_id, "Введите любой ✨advice✨, который может помочь человеку стать более продуктивным.",
	                 reply_markup=markup)


def display_random_advice(chat_id, advice):
	markup = ReplyKeyboardMarkup(resize_keyboard=True)
	markup.add(KeyboardButton('Назад'))
	bot.send_message(chat_id, advice, reply_markup=markup)


@bot.message_handler(commands=['start'])
def on_start(message):
	chat_id = message.chat.id
	bot.send_message(
		chat_id,
		'Приветствую тебя в нашем боте!🤩😿😁'
	)
	bot.send_message(
		chat_id,
		'Данный чат-бот сделали студенты группы Б9123-01.03.02сп: '
		'Пырков Василий😍, Шелевой Ярослав🤡, Вонгай Андрей✨')
	display_main_menu(chat_id)


@bot.message_handler(content_types=['text'])
def on_message(message):
	chat_id = message.chat.id
	if message.text == 'Выйти':
		display_goodbye(chat_id)

	elif informator.is_getting_advice():
		informator.add_advice(message.text)
		informator.state_getting_advice_turn()
		display_advice_answer(chat_id)

	elif message.text == 'Полезная информация':
		display_information(chat_id)

	elif message.text == 'Назад':
		display_main_menu(chat_id)

	elif message.text == "Обратная связь":
		display_set_advice_menu(chat_id)
		informator.state_getting_advice_turn()

	elif message.text == "Получить случайный совет от пользователя":
		display_random_advice(chat_id, informator.get_random_advice())

	else:
		display_error_text(chat_id)


if __name__ == "__main__":
	bot.infinity_polling()
