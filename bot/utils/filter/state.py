from aiogram.fsm.state import State, StatesGroup


class UpdateTimeState(StatesGroup):
     time = State()
     
     
class SearchState(StatesGroup):
     item = State()
     
     
class PercentState(StatesGroup):
     percent = State()