import random, requests


class Client:


    U_A = [
            "Mozilla/5.0 (Linux; Android 9; vivo 1723) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.73 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 11; M2010J19SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.73 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 11; SM-A225F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.73 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 11; LM-V500N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.73 Mobile Safari/537.36"
    ]

    def __init__(self, access_token=None, refresh_token=None, user_id=None, email=None):
        
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.user_id = user_id
        self.email = email

        self._user_agent = random.choice(Client.U_A)
        self._session = requests.Session()
        self._session.headers = self._headers

    
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

