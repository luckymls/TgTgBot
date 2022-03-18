from src.Client import Client


email = "melis.luca2014@gmail.com"
client = Client(email=email)
access_data = client.get_credentials()

access_token = access_data['access_token']
refresh_token =  access_data['refresh_token']
user_id = access_data['user_id']

client = Client(access_token, refresh_token, user_id, email)

items_faved = client.get_faved_item(with_stock=False)

