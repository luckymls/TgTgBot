import firebase_admin

cred_obj = firebase_admin.credentials.Certificate('....path to file')
default_app = firebase_admin.initialize_app(cred_object, {
	'databaseURL':https://test-7f6c4-default-rtdb.europe-west1.firebasedatabase.app/
	})
