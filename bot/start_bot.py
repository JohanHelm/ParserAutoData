from subprocess import run
from loguru import logger
from time import perf_counter

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from utils.mark_duration import duration
from settings import TOKEN, OWNER_ID, DEVELOPER_ID
from app import MainAppManager


bot = Bot(token=TOKEN)
dp = Dispatcher()


drom_launch_btn = InlineKeyboardButton(text="Парсить Дром", callback_data="launch_drom_app")
dvorniki_launch_btn = InlineKeyboardButton(text="Парсить Дворники", callback_data="launch_dvorniki_app")
update_btn = InlineKeyboardButton(text="Обновить!", callback_data="try_to_update")
get_vm_ip_btn = InlineKeyboardButton(text="Проверить ip виртуалки", callback_data="check_vm_ipv4")
keyboard = InlineKeyboardMarkup(inline_keyboard=[[drom_launch_btn], [dvorniki_launch_btn], [get_vm_ip_btn]])


async def process_start_command(message: Message):
    if message.from_user.id == OWNER_ID or message.from_user.id == DEVELOPER_ID:
        await message.answer("Привет, Евгений!!\nБот готов к работе, для запуска программы нажми кнопку Пуск!",
                             reply_markup=keyboard)
        logger.info(f"{message.from_user.id} have started bot")
    else:
        await message.answer("Ты еще слишком мал чтобы пользоваться этим ботом!\nВсего тебе доброго, дружище!!")
        logger.warning(f"Some guy with {message.from_user.id} tried to use this bot")


async def process_help_command(message: Message):
    await message.answer(
        "Для запуска процесса сбора данных с Дрома нажми кнопку Парсить Дром!\n\n"
        "Для запуска процесса сбора данных с Дворников нажми кнопку Парсить Двооники!")


async def start_drom_collect_app(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Сбор данных с дрома начался, ждите!!\nПосле завершения сбора данных вы получите сообщение.')
    main_app_manager = MainAppManager(start_passenger_drom=True, start_freight_drom=True, start_dvorniki=False)
    start = perf_counter()
    main_app_manager.start_main_app()
    end = perf_counter()
    await callback.message.edit_text(text=f'Сбор данных с дрома завершён за {duration(start, end)}!!',
                                     reply_markup=callback.message.reply_markup)


async def start_dvorniki_collect_app(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Сбор данных с дворников, ждите!!\nПосле завершения сбора данных вы получите сообщение.')
    main_app_manager = MainAppManager(start_passenger_drom=False, start_freight_drom=False, start_dvorniki=True)
    start = perf_counter()
    main_app_manager.start_main_app()
    end = perf_counter()
    await callback.message.edit_text(text=f'Сбор данных с дворников завершён за {duration(start, end)}!!\n',
                                     reply_markup=callback.message.reply_markup)


async def check_vm_ipv4_address(callback: CallbackQuery):
    iface_name = ": ens33: "
    result = run(["ip", "-4", "addr"], capture_output=True, text=True).stdout.split("\n")
    stroka = [stroka for stroka in result if iface_name in stroka]
    if stroka:
        position = result.index(stroka[0])
        for i in range(position, len(result)):
            if result[i].startswith("    inet "):
                stroka_with_address = result[i].strip()
                ipv4_addr = stroka_with_address.split()[1]
                await callback.message.edit_text(f"ip v4 адрес виртуалки\n{ipv4_addr}",
                                                 reply_markup=callback.message.reply_markup)
                break
    else:
        await callback.message.edit_text(f"{iface_name} is not found on this vm",
                                         reply_markup=callback.message.reply_markup)


dp.message.register(process_start_command, Command(commands="start"))
dp.message.register(process_help_command, Command(commands="help"))
dp.callback_query.register(start_drom_collect_app, F.data == "launch_drom_app")
dp.callback_query.register(start_dvorniki_collect_app, F.data == "launch_dvorniki_app")
dp.callback_query.register(check_vm_ipv4_address, F.data == "check_vm_ipv4")


async def start_bot():
    logger.info(f"{bot} is on polling")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
