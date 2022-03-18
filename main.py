from src.Client import Client
from src.utils.item_price import item_price


email = "melis.luca2014@gmail.com"
#client = Client(email=email)
#access_data = client.get_credentials()
access_data = {'access_token': 'e30.eyJzdWIiOiIxMzU3MzUyMiIsImV4cCI6MTY0Nzc5MDc1MSwidCI6IkRpQXp6Z2t0VDkyT3lVQjNxVzdvd0E6MDoxIn0.k1n3Rt1f_xMqC0C57OkAbimUfU-_q2GpVGfKxVSeTv4', 'refresh_token': 'e30.eyJzdWIiOiIxMzU3MzUyMiIsImV4cCI6MTY3OTE1Mzk1MSwidCI6Il9PSmVqVHZZUktDclVpeG1PYTlqVFE6MDowIn0.ebKok4XX2uw0gMgjxqjWXqU_IkOAb8mcF48CqTocNIQ', 'user_id': '13573522'}
access_token = access_data['access_token']
refresh_token =  access_data['refresh_token']
user_id = access_data['user_id']

client = Client(access_token, refresh_token, user_id, email)

items_faved = client.get_faved_item(with_stock=False)


for store in items_faved:
    item = store['item']['item_id']
    print(item)
    minor_units = store['item']['price_including_taxes']['minor_units']
    decimal = store['item']['price_including_taxes']['decimals']
    price = item_price(minor_units, decimal)
    store_id = store['store']['store_id']
    store_name = store['store']['store_name']

    items_available = store['items_available']
    new_item = store['new_item'] #true/false
    
    print("%s [%s]" % (store_name, store_id))
    print("Prezzo: %s€" % price)
    print("Magicbox disponibili: %s" % items_available)
    print("\n--------------")
