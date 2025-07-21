from aiogram.fsm.state import State, StatesGroup


class SkinSearchState(StatesGroup):
     skin = State()
     
     
class SkinPercentState(StatesGroup):
     percent = State()
     
     
class SteamIDState(StatesGroup):
     steam_id = State()