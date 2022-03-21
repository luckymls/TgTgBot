from src.Client import Client
from src.utils.store_message import get_store_message
from src.notifier.main import Notifier
from src.tg.Tg import Tg
from db.Database import Database
import threading

import time

bot_token = ""


bot = Tg(bot_token)


def handle(msg):
    content_type, chat_id, txt = bot.msgData(msg)

    if content_type == 'text':

        db = Database()
        if txt == "/start":
            bot.sendMessage(chat_id, "Ciao!\nSono il bot di TooGoodToGo, ti avviserò quando la magicbox dei tuoi negozi preferiti sarà disponibile.\nPer iniziare digita /email tuamail@dominio.com  e al suo posto scrivi la tua mail.\nAssicurati di avere un dispositivo per leggere le mail a portata di mano.\n\n COMANDI\n\n/email tuamail@dominio.com per impostare la tua mail di TgTg\n/store per visualizzare gli store preferiti\n/update lo usi quando metti un nuovo store tra i preferiti e vuoi aggiornare la lista del bot")


        if txt.startswith("/email") and len(txt) > 8:
            
            check_user = db.fetch(f"SELECT * from utenti where user_id='{chat_id}'")
            if len(check_user) == 0:
                email = txt.split("/email ")[1]
                bot.sendMessage(chat_id, "Utente nuovo... Configurazione in corso...")
                
                client = Client(email=email)
                bot.sendMessage(chat_id, "Controlla la casella di posta dal computer e consenti l'accesso. Tempo rimanente 2 minuti...")
                access_data = client.get_credentials()
                access_token = access_data['access_token']
                refresh_token =  access_data['refresh_token']
                tgtg_id = access_data['user_id']
                db.query(f"INSERT INTO utenti (user_id, email, token, r_token, tgtg_id) VALUES ('{chat_id}', '{email}', '{access_token}', '{refresh_token}', '{tgtg_id}')")

                items_faved = client.get_faved_item(with_stock=False)
                store_faved_msg = get_store_message(items_faved)
                bot.sendMessage(chat_id, "Accesso eseguito correttamente.")
                bot.sendMessage(chat_id, store_faved_msg)
            else:
                email = check_user[0][1]
                access_token = check_user[0][2]
                refresh_token = check_user[0][3]
                tgtg_id = check_user[0][4]
                client = Client(access_token, refresh_token, tgtg_id, email)

                items_faved = client.get_faved_item(with_stock=False)
                 
                for item in items_faved:
                    item_id  = item['item']['item_id']
                    items_available = item['items_available']
                    check_item  = db.fetch(f"SELECT * from queue where item_id='{item_id}' and user_id='{chat_id}'")
                    if len(check_item) == 0:
                        db.query(f"INSERT INTO queue (user_id, item_id, last_value) VALUES ('{chat_id}', '{item_id}', '{items_available}')")
                    else:
                        db.query(f"UPDATE queue set last_value='{items_available}' WHERE user_id='{chat_id}' and item_id='{item_id}'")

                store_faved_msg = get_store_message(items_faved)
                bot.sendMessage(chat_id, store_faved_msg)

        if txt == "/store":
            check_user = db.fetch(f"SELECT * from utenti where user_id='{chat_id}'")
            email = check_user[0][1]
            access_token = check_user[0][2]
            refresh_token = check_user[0][3]
            tgtg_id = check_user[0][4]
            client = Client(access_token, refresh_token, tgtg_id, email)

            items_faved = client.get_faved_item(with_stock=True)

            for item in items_faved:
                item_id  = item['item']['item_id']
                items_available = item['items_available']
                check_item  = db.fetch(f"SELECT * from queue where item_id='{item_id}' and user_id='{chat_id}'")
                if len(check_item) == 0:
                    db.query(f"INSERT INTO queue (user_id, item_id, last_value) VALUES ('{chat_id}', '{item_id}', '{items_available}')")
                else:
                    db.query(f"UPDATE queue set last_value='{items_available}' WHERE user_id='{chat_id}' and item_id='{item_id}'")


            store_faved_msg = get_store_message(items_faved)
            bot.sendMessage(chat_id, store_faved_msg)

            


        if txt == "/update":
            check_user = db.fetch(f"SELECT * from utenti where user_id='{chat_id}'")
            email = check_user[0][1]
            access_token = check_user[0][2]
            refresh_token = check_user[0][3]
            tgtg_id = check_user[0][4]
            client = Client(access_token, refresh_token, tgtg_id, email)
            items_faved = client.get_faved_item(with_stock=False)
            
            for item in items_faved:
                item_id  = item['item']['item_id']
                items_available = item['items_available']
                check_item  = db.fetch(f"SELECT * from queue where item_id='{item_id}' and user_id='{chat_id}'")
                if len(check_item) == 0:
                    db.query(f"INSERT INTO queue (user_id, item_id, last_value) VALUES ('{chat_id}', '{item_id}', '{items_available}')")
                else:
                    db.query(f"UPDATE queue set last_value='{items_available}' WHERE user_id='{chat_id}' and item_id='{item_id}'")


            bot.sendMessage(chat_id, "Store preferiti aggiornati.")



bot.messageListener(handle)

threading.Thread(target= lambda i=1: Notifier(bot.sendMessage)).start()

while 1:
    time.sleep(1)

