import telepot
from telepot.loop import MessageLoop

class Tg:


    def __init__(self, token):
        self.token = token
        self.connect()

    def connect(self):
        self.bot = telepot.Bot(self.token)

    def getMe(self):
        return self.bot.getMe()

    def sendMessage(self, user, msg):
        self.bot.sendMessage(user, msg)

    def messageListener(self, handle):
        MessageLoop(self.bot, handle).run_as_thread()

    def msgData(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if "text" in msg:
            text = msg['text']
        return (content_type, chat_id, text)
    