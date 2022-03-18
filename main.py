from src.Client import Client


email = ""
client = Client(email)
access_data = client.get_credentials()

access_token = access_data['access_token']
refresh_token =  access_data['refresh_token']
user_id = access_data['user_id']

client = Client(access_token, refresh_token, user_id)

items_faved = client.get_items()

