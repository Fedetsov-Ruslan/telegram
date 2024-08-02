import httpx
import logging

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

user_private_router = Router()

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
    await message.answer("Привет")

@user_private_router.message(Command('show'))
async def show_messages(message: Message):
    user_name = message.from_user.username
    route = "http://fastapi_messages:8001/api/v1/messages/"
    response = await send_to_api(route, user_name, "", method="get")
    
    if response.status_code == 200:
        messages = response.json()
        print(messages['messages'])
        answers = [f"{user}: {mess}" for user, mess in zip(messages['users'], messages['messages'])]

        await message.answer("\n".join(answers))
    else:
        await message.answer("Не удалось получить сообщения.")

@user_private_router.message()
async def write_message(message: Message):
    user_name = message.from_user.username
    message_text = message.text
    route = "http://fastapi_messages:8001/api/v1/message/"
    await send_to_api(route, user_name, message_text)
    await message.answer('сообщение доставлено')
