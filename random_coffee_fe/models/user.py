from aiogram.dispatcher.filters.state import State, StatesGroup

class UserStates(StatesGroup):
    INIT = State()
    WAITING_NAME = State()
    EMAIL_SENT = State()
    WAITING_MODERATION = State()
    ONBOARDING = State()
    READY_STATUS = State()
    CLUBS = State()
    CREATE_MEETING = State()

class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.state = UserStates.INIT
        self.name = None
        self.clubs = []
        self.ready_status = False