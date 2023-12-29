
import configparser
import requests
import logging

class MoodleAPI:

    MOODLE_API_URL = "https://moodle.htw-berlin.de/webservice/rest/server.php"
    MOODLE_API_TOKEN = "5c1188948fdc76b65150cbee75506c8a"

    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.url = self.config["moodle"]["moodleUrl"]
        self.session = requests.Session()
        self.request_header = {
            "User-Agent": (
                "Mozilla/5.0 (Linux; Android 7.1.1; Moto G Play Build/NPIS26.48-43-2; wv) AppleWebKit/537.36"
                + " (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.99 Mobile Safari/537.36 MoodleMobile"
            ),
            "Content-Type": "application/x-www-form-urlencoded",
        }
        self.session.headers.update(self.request_header)
        self.token = None
        self.userid = None

    @classmethod
    def headers(cls):
        return {
            "Authorization": f"Bearer {cls.MOODLE_API_TOKEN}",
            "Content-Type": "application/json",
        }

    def login(self, username, password):
        login_data = {
            "username": username,
            "password": password,
            "service": "moodle_mobile_app",
        }
        response = self.session.post(f"{self.url}login/token.php", data=login_data)
        if "token" in response.text and "privatetoken" in response.text:
            logging.info("Login successful")
            self.token = response.json()["token"]
            return True
        else:
            logging.error("Login failed")
            return False

    def get_site_info(self):
        if self.token is None:
            logging.error("Token not set. Please login first.")
            return None
        wsfunction = "core_webservice_get_site_info"
        params = {
            "wstoken": self.token,
            "wsfunction": wsfunction,
            "moodlewsrestformat": "json",
        }
        response = self.session.post(f"{self.url}webservice/rest/server.php", params=params)
        self.userid = response.json()["userid"]
        return response.json()

    def get_popup_notifications(self, user_id):
        return self._post("message_popup_get_popup_notifications", user_id)

    def popup_notification_unread_count(self, user_id):
        return self._post("message_popup_get_unread_popup_notification_count", user_id)

    def _post(self, wsfunction, user_id):
        if self.token is None:
            logging.error("Token not set. Please login first.")
            return None
        params = {
            "wstoken": self.token,
            "wsfunction": wsfunction,
            "useridto": user_id,
            "moodlewsrestformat": "json",
        }
        response = self.session.post(f"{self.url}webservice/rest/server.php", params=params)
        return response.json()

def get_moodle_data():
    params = {
        "wstoken": MoodleAPI.MOODLE_API_TOKEN,
        "moodlewsrestformat": "json",
    }
    response = requests.get(MoodleAPI.MOODLE_API_URL, params=params, headers=MoodleAPI.headers())
    print("Get Moodle Data Response:", response.text)
    data = response.json()
    return data

def post_moodle_data(data_to_post):
    params = {
        "wstoken": MoodleAPI.MOODLE_API_TOKEN,
        "moodlewsrestformat": "json",
    }
    response = requests.post(MoodleAPI.MOODLE_API_URL, params=params, headers=MoodleAPI.headers(), json=data_to_post)
    print("Post Moodle Data Response:", response.text)
    result = response.json()
    return result
