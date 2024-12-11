from random_coffee_be.models.user import User

class UserManager:
    def init(self):
        self.users = {}

def get_user(self, chat_id):
    if chat_id not in self.users:
        self.users[chat_id] = User(chat_id)
    return self.users[chat_id]