from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message, ContentTypes
from collections import defaultdict, Counter
from aiogram.dispatcher import FSMContext
from states import Users
from typing import List
from loader import dp


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
    await state.update_data({"tp_list": list(map(int, message.text.split()))})
    await message.answer("SP ma'lumotlarni yuboring!")
    await Users.one.set()


@dp.message_handler(content_types=ContentTypes.TEXT, state=Users.one)
async def answer_name(message: Message, state: FSMContext):
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
    await message.answer(
        f"Kiritilgan sonni indeks qiymati:={len(filtered_tp)}\n{filtered_tp}\n"
        f"Tegishli qiymatlar: {await extract_sp_values(tp_numbers, sp_numbers, filtered_tp)}")
    await message.answer(f"Tartiblangan ruyhat:{sorted_numbers}")
    await message.answer(f"sp ma'lumotlari:{sp_numbers}")
    await message.answer(f"Kerakli sonni kiriting:")
    await Users.two.set()
