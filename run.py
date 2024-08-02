import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import  Update
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from handlers.user_privare import user_private_router

load_dotenv()

bot = Bot(token=os.getenv("TG_TOKEN"))
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(user_private_router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    webhook_url = 'https://091e-37-128-205-168.ngrok-free.app/webhook'
    await bot.set_webhook(webhook_url)
    yield
    await bot.delete_webhook()

app = FastAPI(lifespan=lifespan)

@app.post("/webhook")
async def webhook(request: Request):
    try:
        json_data = await request.json()
        logging.info(f"Received data: {json_data}")
        update = Update.model_validate(json_data, context={"bot": bot})
        await dp.feed_update(bot, update)
        return {"status": "ok"}
    except Exception as e:
        logging.error(f"Error processing update: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8000)

