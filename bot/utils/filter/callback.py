from aiogram.filters.callback_data import CallbackData



class SkinNameCallbackData(CallbackData, prefix="?"):
     mode: str
     name: str