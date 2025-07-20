from aiogram.fsm.state import State, StatesGroup


class SearchState(StatesGroup):
     item = State()
     
     
class PercentState(StatesGroup):
     percent = State()
     
     
class SteamIDState(StatesGroup):
     steamid = State()