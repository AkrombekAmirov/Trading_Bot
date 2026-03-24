from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message, ContentTypes
from collections import defaultdict, Counter
from aiogram.dispatcher import FSMContext
from states import Users
from typing import List
from loader import dp

MAX_TG_MESSAGE = 4000  # Telegram safe limit

async def send_long_message(message: Message, text: str):
    """
    Telegram 4096 limitidan oshadigan xabarlarni bo‘lib yuboradi.
    Asosiy mantiqqa tegmaydi.
    """
    for i in range(0, len(text), MAX_TG_MESSAGE):
        await message.answer(text[i:i + MAX_TG_MESSAGE])


def custom_round(x):
    if x - int(x) == 0.5:
        return int(x) + 1
    return round(x)


async def extract_sp_values(tp_list: List[int], sp_list: List[int], extracted_values: List[int]) -> List[int]:
    value_counts = Counter(extracted_values)
    tp_index_map = defaultdict(list)

    for idx, val in enumerate(tp_list):
        tp_index_map[val].append(idx)

    # Endi kerakli sonlar uchun sp qiymatlarini topamiz
    result_sp_values = []

    for val in extracted_values:
        if tp_index_map[val]:
            tp_idx = tp_index_map[val].pop(0)  # Faqat birinchi mavjud indeksni olib tashlaymiz
            result_sp_values.append(sp_list[tp_idx])
        else:
            result_sp_values.append(None)  # Bunday bo'lishi kerak emas, ammo ehtiyot chora sifatida

    return result_sp_values


@dp.message_handler(CommandStart())
async def bot_start(message: Message):
    await message.answer(f"Salom, {message.from_user.full_name}!\n TP ma'lumotlarni yuboring!")
    await Users.zero.set()


@dp.message_handler(content_types=ContentTypes.TEXT, state=Users.zero)
async def answer_name(message: Message, state: FSMContext):
    if message.text == "/start":
        await message.answer(f"Salom, {message.from_user.full_name}! \n TP ma'lumotlarni yuboring!")
        await Users.zero.set()
        return
    await state.update_data({"tp_list": list(map(int, message.text.split()))})
    await message.answer("SP ma'lumotlarni yuboring!")
    await Users.one.set()


@dp.message_handler(content_types=ContentTypes.TEXT, state=Users.one)
async def answer_name(message: Message, state: FSMContext):
    if message.text == "/start":
        await message.answer(f"Salom, {message.from_user.full_name}! \n TP ma'lumotlarni yuboring!")
        await Users.zero.set()
        return
    await state.update_data({"sp_list": list(map(int, message.text.split()))})
    await message.answer("Kerakli sonni kiriting:")
    await Users.two.set()


@dp.message_handler(content_types=ContentTypes.TEXT, state=Users.two)
async def answer_name(message: Message, state: FSMContext, raw_state: FSMContext):
    if message.text == "/start":
        await message.answer(f"Salom, {message.from_user.full_name}!\n TP ma'lumotlarni yuboring!")
        await Users.zero.set()
        return
    limit = int(message.text)
    data = await state.get_data()
    tp_numbers = data.get("tp_list")
    sp_numbers = data.get("sp_list")
    sorted_numbers = sorted(tp_numbers)
    filtered_tp = [x for x in sorted_numbers if x <= limit]
    text = (
        f"Kiritilgan sonni indeks qiymati:={len(filtered_tp)}\n{filtered_tp}\n"
        f"Tegishli qiymatlar: {await extract_sp_values(tp_numbers, sp_numbers, filtered_tp)}")
    await send_long_message(message, text)
    await message.answer(f"Tartiblangan ruyhat:{sorted_numbers}")
    await message.answer(f"sp ma'lumotlari:{sp_numbers}")
    await message.answer(f"Kerakli sonni kiriting:")
    await Users.two.set()
    # ------------------------------------------------------------------
# import logging
# from aiogram.dispatcher import FSMContext
# from aiogram import Bot, Dispatcher, executor, types
# from aiogram.dispatcher.filters.builtin import CommandStart
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.types import Message, ContentTypes
# from collections import defaultdict, Counter
# from typing import List
# # =========================
# # 🔐 BOT TOKEN
# # =========================
# BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"
#
# # =========================
# # LOGGING
# # =========================
# logging.basicConfig(level=logging.INFO)
#
# # =========================
# # BOT INIT
# # =========================
# bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
# storage = MemoryStorage()
# dp = Dispatcher(bot, storage=storage)
#
# # =========================
# # FSM STATES
# # =========================
# class Users(StatesGroup):
#     zero = State()
#     one = State()
#     two = State()
#
# # =========================
# # CONSTANTS
# # =========================
# MAX_TG_MESSAGE = 4000  # Telegram safe limit
#
# # =========================
# # HELPERS
# # =========================
# async def send_long_message(message: Message, text: str):
#     """
#     Telegram 4096 limitidan oshadigan xabarlarni bo‘lib yuboradi.
#     Asosiy mantiqqa tegmaydi.
#     """
#     for i in range(0, len(text), MAX_TG_MESSAGE):
#         await message.answer(text[i:i + MAX_TG_MESSAGE])
#
#
# def custom_round(x):
#     if x - int(x) == 0.5:
#         return int(x) + 1
#     return round(x)
#
#
# async def extract_sp_values(tp_list: List[int], sp_list: List[int], extracted_values: List[int]) -> List[int]:
#     value_counts = Counter(extracted_values)
#     tp_index_map = defaultdict(list)
#
#     for idx, val in enumerate(tp_list):
#         tp_index_map[val].append(idx)
#
#     # Endi kerakli sonlar uchun sp qiymatlarini topamiz
#     result_sp_values = []
#
#     for val in extracted_values:
#         if tp_index_map[val]:
#             tp_idx = tp_index_map[val].pop(0)  # Faqat birinchi mavjud indeksni olib tashlaymiz
#             result_sp_values.append(sp_list[tp_idx])
#         else:
#             result_sp_values.append(None)  # Bunday bo'lishi kerak emas, ammo ehtiyot chora sifatida
#
#     return result_sp_values
#
# # =========================
# # HANDLERS
# # =========================
# @dp.message_handler(CommandStart())
# async def bot_start(message: Message):
#     await message.answer(f"Salom, {message.from_user.full_name}!\n TP ma'lumotlarni yuboring!")
#     await Users.zero.set()
#
#
# @dp.message_handler(content_types=ContentTypes.TEXT, state=Users.zero)
# async def answer_name(message: Message, state: FSMContext):
#     if message.text == "/start":
#         await message.answer(f"Salom, {message.from_user.full_name}! \n TP ma'lumotlarni yuboring!")
#         await Users.zero.set()
#         return
#     await state.update_data({"tp_list": list(map(int, message.text.split()))})
#     await message.answer("SP ma'lumotlarni yuboring!")
#     await Users.one.set()
#
#
# @dp.message_handler(content_types=ContentTypes.TEXT, state=Users.one)
# async def answer_name(message: Message, state: FSMContext):
#     if message.text == "/start":
#         await message.answer(f"Salom, {message.from_user.full_name}! \n TP ma'lumotlarni yuboring!")
#         await Users.zero.set()
#         return
#     await state.update_data({"sp_list": list(map(int, message.text.split()))})
#     await message.answer("Kerakli sonni kiriting:")
#     await Users.two.set()
#
#
# @dp.message_handler(content_types=ContentTypes.TEXT, state=Users.two)
# async def answer_name(message: Message, state: FSMContext, raw_state: FSMContext):
#     if message.text == "/start":
#         await message.answer(f"Salom, {message.from_user.full_name}!\n TP ma'lumotlarni yuboring!")
#         await Users.zero.set()
#         return
#     limit = int(message.text)
#     data = await state.get_data()
#     tp_numbers = data.get("tp_list")
#     sp_numbers = data.get("sp_list")
#     sorted_numbers = sorted(tp_numbers)
#     filtered_tp = [x for x in sorted_numbers if x <= limit]
#     text = (
#         f"Kiritilgan sonni indeks qiymati:={len(filtered_tp)}\n{filtered_tp}\n"
#         f"Tegishli qiymatlar: {await extract_sp_values(tp_numbers, sp_numbers, filtered_tp)}")
#     await send_long_message(message, text)
#     await message.answer(f"Tartiblangan ruyhat:{sorted_numbers}")
#     await message.answer(f"sp ma'lumotlari:{sp_numbers}")
#     await message.answer(f"Kerakli sonni kiriting:")
#     await Users.two.set()
#
# # =========================
# # RUN
# # =========================
# if __name__ == "__main__":
#     executor.start_polling(dp, skip_updates=True)
