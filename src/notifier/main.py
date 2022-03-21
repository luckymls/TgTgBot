from db.Database import Database
from src.Client import Client
import time


class Notifier:


    def __init__(self, f_notifier):

        self.db = Database()
        print("Notifier Started.")
        self.start(f_notifier)


    def start(self, f_notifier):
        
        while True:
            check_item = self.db.fetch("SELECT * from queue")
            
            for item in check_item:

                db_user_id = item[0]
                db_item_id = item[1]
                last_value = item[2]

                check_user = self.db.fetch(f"SELECT * from utenti where user_id='{db_user_id}'")

                
                email = check_user[0][1]
                access_token = check_user[0][2]
                refresh_token = check_user[0][3]
                tgtg_id = check_user[0][4]
                client = Client(access_token, refresh_token, tgtg_id, email)

                c_item = client.get_item(db_item_id)

                
                item_id  = c_item['item']['item_id']
                items_available = c_item['items_available']
                store_id = c_item['store']['store_id']
                store_name = c_item['store']['store_name']

                if int(items_available) != int(last_value):
                    f_notifier(db_user_id, "%s magicbox disponibili in %s [%s]" % (items_available, store_name, store_id))
                    self.db.query(f"UPDATE queue set last_value='{items_available}' WHERE user_id='{db_user_id}' and item_id='{item_id}'")
            

            check_user = self.db.fetch(f"SELECT * from utenti")

            for user in check_user:
                chat_id = user[0]
                email = user[1]
                access_token = user[2]
                refresh_token = user[3]
                tgtg_id = user[4]
                
                client = Client(access_token, refresh_token, tgtg_id, email)
                
                self.db.fetch(f"SELECT * from queue where user_id='{chat_id}'")
                
                items_faved = client.get_faved_item(with_stock=False)

                for item in items_faved:
                    item_id  = item['item']['item_id']
                    store_id = item['store']['store_id']
                    store_name = item['store']['store_name']
                    check_item  = self.db.fetch(f"SELECT * from queue where item_id='{item_id}' and user_id='{chat_id}'")
                    if len(check_item) == 0:
                        self.db.query(f"INSERT INTO queue (user_id, item_id, last_value) VALUES ('{chat_id}', '{item_id}', '{items_available}')")
                        f_notifier(db_user_id, "%s [%s] nuovo store aggiunto alla lista." % (store_name, store_id))


            time.sleep(10)