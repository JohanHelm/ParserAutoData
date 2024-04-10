from os import chdir, getcwd
from os.path import expanduser
from subprocess import PIPE, Popen
from loguru import logger
import time

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from settings import TOKEN, DEVELOPER_ID, OWNER_ID
from app import MainAppManager


bot = Bot(token=TOKEN)
dp = Dispatcher()


launch_button = InlineKeyboardButton(text="Пуск!", callback_data="launch_the_app")
update_buton = InlineKeyboardButton(text="Обновить!", callback_data="try_to_update")
keyboard = InlineKeyboardMarkup(inline_keyboard=[[launch_button], [update_buton]])


async def process_start_command(message: Message):
    if message.from_user.id in (DEVELOPER_ID, OWNER_ID):
        await message.answer("Привет, бот готов к работе, для запуска программы нажми кнопку Пуск!",
                             reply_markup=keyboard)
        logger.info(f"{message.from_user.id} have started bot")
    else:
        await message.answer("Ты еще слишком мал чтобы пользоваться этим ботом!\nВсего тебе доброго, дружище!!")
        logger.warning(f"Some guy with {message.from_user.id} tryed to use this bot")


async def process_help_command(message: Message):
    await message.answer(
        "Для запуска процесса сбора данных с сайтов нажми кнопку ▶️Пуск!\n\n"
        "Для обновления программы нажми кнопку 🔼Обновить!\n\n"
        "Если обновление прошло успешно то ты получишь сообщение и виртуалка будет перезапущена")


async def process_launch_app(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Сбор данных начался, ждите!!\nПосле завершения сбора данных вы получите сообщение.')
    main_app_manager = MainAppManager(start_passenger_drom=False, start_freight_drom=True, start_dvorniki=False)
    main_app_manager.start_main_app()
    await callback.message.edit_text(text='Сбор данных завершён!! Для повторого сбора данных нажмите кнопку Пуск!',
                                     reply_markup=callback.message.reply_markup)


async def check_for_updates(callback: CallbackQuery):
    # current_directory = getcwd()
    # chdir(f'{expanduser("~")}/.local/share/cli_youtube/')
    cmd = f'git pull origin main '
    update_request = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True)
    update_result = update_request.communicate()[0]
    if 'Already up to date.\n' in update_result:
        # chdir(current_directory)
        await callback.message.edit_text(text="Приложение в актуальном состоянии, обновление не требуется.",
                                         reply_markup=callback.message.reply_markup)
    else:
        await callback.message.edit_text(text="Приложение было обновлено. Сейчас приложение будет перезапущено.\n"
                                              "Подождите одну минуту и перезапустите бота.")





dp.message.register(process_start_command, Command(commands="start"))
dp.message.register(process_help_command, Command(commands="help"))
dp.callback_query.register(process_launch_app, F.data == "launch_the_app")
dp.callback_query.register(check_for_updates, F.data == "try_to_update")



async def start_bot():
    logger.info(f"{bot} is on polling")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)





