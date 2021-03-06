import time, random, requests, datetime


class Client:


    U_A = [
            "Mozilla/5.0 (Linux; Android 9; vivo 1723) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.73 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 11; M2010J19SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.73 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 11; SM-A225F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.73 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 11; LM-V500N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.73 Mobile Safari/537.36"
    ]

    BASE = "https://apptoogoodtogo.com/api/"
    FETCH_ENDPOINT = BASE+"auth/v3/token/refresh"
    LOGIN_ENDPOINT = BASE+"auth/v3/authByEmail"
    POLLING_ENDPOINT = BASE+"auth/v3/authByRequestPollingId"
    ITEM_ENDPOINT = BASE+"item/v7/"

    def __init__(self, access_token=None, refresh_token=None, user_id=None, email=None):
        
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.user_id = user_id
        self.email = email

        
        
        self._user_agent = random.choice(Client.U_A)
        self.session = requests.Session()
        self.session.headers = self._headers

        self.logged_in = False
        if self.access_token and self.refresh_token and self.user_id:
            self.logged_in=True
        self.token_was_refreshed_at = None
    
    @property
    def _headers(self):
        
        headers = {
            "user-agent": self._user_agent,
            "accept-language": "it-IT",
            "Accept-Encoding": "gzip",
        }
        if self.access_token:
            headers["authorization"] = "Bearer "+self.access_token
        return headers 

    def get_credentials(self):
        self.login()
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "user_id": self.user_id
        }
    

    @property
    def refresh_token_valid(self):
        if self.token_was_refreshed_at and (datetime.datetime.now() - self.token_was_refreshed_at).seconds <= 14400:
            return True
        return False

    def fetch_new_token(self):
        
        payload = {'refresh_token': self.refresh_token}

        r = self.session.post(Client.FETCH_ENDPOINT, json=payload,headers=self._headers)
            
        if r.status_code == 200:
            self.access_token = r.json()["access_token"]
            self.refresh_token = r.json()["refresh_token"]
            self.token_was_refreshed_at = datetime.datetime.now()
        else:
            print("Errore ottenendo nuovo token: %s" % str(r.text))


    def login(self):
        
        if self.logged_in:
            if self.refresh_token_valid == False:
                self.fetch_new_token()

        else:

            payload = {"device_type": "ANDROID", "email": self.email}

            req = self.session.post(Client.LOGIN_ENDPOINT, json=payload, headers=self._headers)
            if req.status_code == 200:
                r = req.json()
                if r["state"] == "TERMS":
                    print("Email never used, user has to sign up first")

                elif r["state"] == "WAIT":
                    self.start_polling(r["polling_id"])
                else:
                    print("Generic error while polling: "+str(req.content))
            else:
                if req.status_code == 429:
                    print("Too many requests made by this IP. Wait...")
                else:
                    print("Generic error: "+str(req.content))


    def start_polling(self, polling_id):

        for _ in range(24):

            data={
                "device_type": "ANDROID",
                "email": self.email,
                "request_polling_id": polling_id,
            }
            response = self.session.post(Client.POLLING_ENDPOINT, json=data, headers=self._headers)
            
            if response.status_code == 202:
                print("New mail on your mailbox, check on PC to continue... \n(Doesn't work on mobile, if you have installed TooGoodToGo app.)")
                time.sleep(6)
                continue
            elif response.status_code == 200:
                print("Successfully logged in")
                self.logged_in=True
                r = response.json()
                self.access_token = r["access_token"]
                self.refresh_token = r["refresh_token"]
                self.token_was_refreshed_at = datetime.datetime.now()
                self.user_id = r["startup_data"]["user"]["user_id"]
                return
            else:
                if response.status_code == 429:
                    print("Too many request, retry in few minutes.")
                else:
                    print("Generic error: "+str(response.content))

        print("Too many retries. You have to be faster checking your mailbox. Retry in few minutes.")



    def get_faved_item(self, with_stock=False):
        self.login()

        payload = {
            "user_id": self.user_id,
            "origin": {"latitude": 0.0, "longitude": 0.0},
            "radius": 21,
            "with_stock_only": with_stock,
            "favorites_only": True,
            "hidden_only": False,
            "we_care_only": False,
            "discover": False,
            "page_size": 20,
            "page": 1,
        }
        response = self.session.post(Client.ITEM_ENDPOINT, json=payload, headers=self._headers)
        if response.status_code == 200:
            return response.json()["items"]
        else:
            print("Error fetching user faved magicbox: "+str(response.content))


    def get_item(self, item_id):
        self.login()

        payload = {
            "user_id": self.user_id,
            "origin": None}
        response = self.session.post(Client.ITEM_ENDPOINT+str(item_id), json=payload, headers=self._headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching item with id: "+ str(item_id))