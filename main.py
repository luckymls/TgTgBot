from src.Client import Client


email = "melis.luca2014@gmail.com"
#client = Client(email=email)
#access_data = client.get_credentials()
access_data = {'access_token': 'e30.eyJzdWIiOiIxMzU3MzUyMiIsImV4cCI6MTY0Nzc5MDc1MSwidCI6IkRpQXp6Z2t0VDkyT3lVQjNxVzdvd0E6MDoxIn0.k1n3Rt1f_xMqC0C57OkAbimUfU-_q2GpVGfKxVSeTv4', 'refresh_token': 'e30.eyJzdWIiOiIxMzU3MzUyMiIsImV4cCI6MTY3OTE1Mzk1MSwidCI6Il9PSmVqVHZZUktDclVpeG1PYTlqVFE6MDowIn0.ebKok4XX2uw0gMgjxqjWXqU_IkOAb8mcF48CqTocNIQ', 'user_id': '13573522'}
access_token = access_data['access_token']
refresh_token =  access_data['refresh_token']
user_id = access_data['user_id']

client = Client(access_token, refresh_token, user_id, email)

items_faved = client.get_faved_item(with_stock=False)
print(items_faved)

