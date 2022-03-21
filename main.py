from src.Client import Client
from src.utils.item_price import item_price
from src.tg.Tg import Tg
from db.Database import Database

import time

bot_token = ""


bot = Tg(bot_token)



def handle(msg):
    content_type, chat_id, txt = bot.msgData(msg)

    if content_type == 'text':

        db = Database()
        if txt == "/start":
            bot.sendMessage(chat_id, "Ciao!\nSono il bot di TooGoodToGo, ti avviserò quando la magicbox dei tuoi negozi preferiti sarà disponibile.\nPer iniziare digita /email tuamail@dominio.com  e al suo posto scrivi la tua mail.\nAssicurati di avere un dispositivo per leggere le mail a portata di mano.")


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
                store_faved_msg = "INIZIO A MONITORARE I SEGUENTI STORE\n\n"
                for store in items_faved:
                
                    item = store['item']['item_id']
                    minor_units = store['item']['price_including_taxes']['minor_units']
                    decimal = store['item']['price_including_taxes']['decimals']
                    price = item_price(minor_units, decimal)
                    store_id = store['store']['store_id']
                    store_name = store['store']['store_name']

                    items_available = store['items_available']
                    
                    store_faved_msg += "%s [%s]\n" % (store_name, store_id)
                    store_faved_msg += "Prezzo: %s€" % price
                    store_faved_msg += "Magicbox disponibili: %s\n" % items_available
                    
                bot.sendMessage(chat_id, store_faved_msg)
            else:
                email = check_user[0][1]
                access_token = check_user[0][2]
                refresh_token = check_user[0][3]
                tgtg_id = check_user[0][4]
                client = Client(access_token, refresh_token, tgtg_id, email)

                items_faved = client.get_faved_item(with_stock=False)
                store_faved_msg = "STORE MONITORATI\n\n"
                for store in items_faved:
                
                    item = store['item']['item_id']
                    minor_units = store['item']['price_including_taxes']['minor_units']
                    decimal = store['item']['price_including_taxes']['decimals']
                    price = item_price(minor_units, decimal)
                    store_id = store['store']['store_id']
                    store_name = store['store']['store_name']

                    items_available = store['items_available']
                    
                    store_faved_msg += "%s [%s]\n" % (store_name, store_id)
                    store_faved_msg += "Prezzo: %s€\n" % price
                    store_faved_msg += "Magicbox disponibili: %s\n\n" % items_available
                    
                bot.sendMessage(chat_id, store_faved_msg)

        if txt == "/store":
            check_user = db.fetch(f"SELECT * from utenti where user_id='{chat_id}'")
            email = check_user[0][1]
            access_token = check_user[0][2]
            refresh_token = check_user[0][3]
            tgtg_id = check_user[0][4]
            client = Client(access_token, refresh_token, tgtg_id, email)

            items_faved = client.get_faved_item(with_stock=False)
            store_faved_msg = "STORE MONITORATI\n\n"
            for store in items_faved:
            
                item = store['item']['item_id']
                minor_units = store['item']['price_including_taxes']['minor_units']
                decimal = store['item']['price_including_taxes']['decimals']
                price = item_price(minor_units, decimal)
                store_id = store['store']['store_id']
                store_name = store['store']['store_name']

                items_available = store['items_available']
                
                store_faved_msg += "%s [%s]\n" % (store_name, store_id)
                store_faved_msg += "Prezzo: %s€\n" % price
                store_faved_msg += "Magicbox disponibili: %s\n\n" % items_available
                
            bot.sendMessage(chat_id, store_faved_msg)



bot.messageListener(handle)

while 1:
    time.sleep(1)

