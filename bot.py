from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import json

API_TOKEN = "API_TOKEN"
MANAGER_CHAT_ID = 1234567890

bot = Bot(API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class ApplicationForm(StatesGroup):
    name = State()
    age = State()
    course_date = State()

@dp.message(F.text == "/start")
async def start(message: types.Message, state: FSMContext):
    await message.answer("Welcome to the programming course registration bot!\nWhat is your name?")
    await state.set_state(ApplicationForm.name)
    print(message)

@dp.message(ApplicationForm.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("How old are you?")
    await state.set_state(ApplicationForm.age)

@dp.message(ApplicationForm.age)
async def get_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("When do you want to start? (e.g. 15.06.2025 16:00)")
    await state.set_state(ApplicationForm.course_date)

@dp.message(ApplicationForm.course_date)
async def get_course_date(message: types.Message, state: FSMContext):
    await state.update_data(course_date=message.text)
    data = await state.get_data()

    user_data = {
        "user_id": message.from_user.id,
        "name": data["name"],
        "age": data["age"],
        "course_date": data["course_date"]
    }

    text = (
        f"📩 New Course Application\n\n"
        f"👤 Name: {user_data['name']}\n"
        f"🎂 Age: {user_data['age']}\n"
        f"📅 Desired Date: {user_data['course_date']}\n"
        f"🆔 User ID: {user_data['user_id']}"
    )

    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Approve", callback_data="approve")],
        [InlineKeyboardButton(text="❌ Reject", callback_data="reject")]
    ]
    )

    await bot.send_message(chat_id=MANAGER_CHAT_ID, text=text, reply_markup=keyboard)
    await message.answer("Your application has been sent. Wait for manager approval.")
    await state.clear()

@dp.callback_query(F.data.startswith("accept"))
async def accept(callback: CallbackQuery):
    raw = callback.data.replace("accept", "")
    data = json.loads(raw)

    await bot.send_message(data["user_id"], "✅ Your application has been *accepted*! We'll see you soon.", parse_mode="Markdown")
    await callback.message.edit_text(callback.message.text + "\n\n✅ Accepted.")

@dp.callback_query(F.data.startswith("reject"))
async def reject(callback: CallbackQuery):
    raw = callback.data.replace("reject", "")
    data = json.loads(raw)

    await bot.send_message(data["user_id"], "❌ Sorry, your application has been *rejected*. Try another time.", parse_mode="Markdown")
    await callback.message.edit_text(callback.message.text + "\n\n❌ Rejected.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
