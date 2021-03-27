class PublicBot():
    def __init__(self, controller):
        self.controller = controller

    def authenticate_invite(self, room, event):
        return True

    def authenticate_message(self, room, event):
        return True

class BlockAll():
    def __init__(self, controller):
        self.controller = controller

    def authenticate_invite(self, room, event):
        return False

    def authenticate_message(self, room, event):
        return False

class UserWhitelist():
    def __init__(self, controller):
        self.controller = controller

    def authenticate_invite(self, room, event):
        try:
            sender = event.sender
            if sender in self.controller.USER_WHITELIST:
                return True
        except:
            return False
        return False

    def authenticate_message(self, room, event):
        try:
            sender = event.sender
            if sender in self.controller.USER_WHITELIST:
                return True
        except:
            return False
        return False
