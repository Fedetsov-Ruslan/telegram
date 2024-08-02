from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def send_page(all_messages: list, page: int):
    items_per_page = 5
    total_pages = (len(all_messages) + items_per_page - 1) // items_per_page
    start = (page - 1) * items_per_page
    end = start + items_per_page
    page_messages = all_messages[start:end]
    page_text = "\n".join(page_messages)

    keyboard = InlineKeyboardBuilder()
    if page > 1:
        keyboard.add(InlineKeyboardButton(text="Предыдущая страница", callback_data=f"page_{page-1}"))
    if page < total_pages: 
        keyboard.add(InlineKeyboardButton(text="Следующая страница", callback_data=f"page_{page+1}"))
    
    return page_text, keyboard.adjust(2,).as_markup()
    