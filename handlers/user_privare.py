import httpx
import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from kbds.inline import send_page


user_private_router = Router()

class PaginationState(StatesGroup):
    all_messages = State()


async def send_to_api(route: str, user_name: str, message_text: str, method:str='POST'):
    async with httpx.AsyncClient() as client:
        if method == 'POST':
            response = await client.post(
                route,
                json={"user_name": user_name, "content": message_text}
            )
        elif method == "get":
            response = await client.get(route)
        if response.status_code != 200:
            logging.error(f"Failed to {method} message: {response.text}")
        return response

@user_private_router.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет!")

@user_private_router.callback_query(F.data.startswith("page_"))
async def handle_pagination(callback: CallbackQuery, state: FSMContext):
    page = int(callback.data.split("_")[1])
    data = await state.get_data()
    all_messages = data['all_messages']
    text, kbds = await send_page( all_messages, page)
    await callback.message.edit_text(text=text, reply_markup=kbds)

@user_private_router.message(Command('show'))
async def show_messages(message: Message, state: FSMContext):
    user_name = message.from_user.username
    route = "http://fastapi_messages:8001/api/v1/messages/"
    response = await send_to_api(route, user_name, "", method="get")
    
    if response.status_code == 200:
        messages = response.json()
        answers = [f"{user}: {mess}" for user, mess in zip(messages['users'], messages['messages'])]
        await state.update_data(all_messages=answers)
        if not answers:
            await message.answer("Сообщений нет")
            return
        text, kbds = await send_page(all_messages=answers, page=1)
        await message.answer(text=text, reply_markup=kbds)
    else:
        await message.answer("Не удалось получить сообщения.")

@user_private_router.message()
async def write_message(message: Message):
    user_name = message.from_user.username
    message_text = message.text
    route = "http://fastapi_messages:8001/api/v1/message/"
    await send_to_api(route, user_name, message_text)
    await message.answer('сообщение доставлено')


