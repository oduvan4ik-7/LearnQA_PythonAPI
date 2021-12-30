from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from lib.assertions import Assertions


class User(BaseCase):
    def __init__(self):
        self.email = None
        self.password = None
        self.username = None
        self.firstName = None
        self.lastName = None
        self.id = None

    def create(self):
        user_data = self.prepare_registration_data()
        self.email = user_data['email']
        self.password = user_data['password']
        self.username = user_data['username']
        self.firstName = user_data['firstName']
        self.lastName = user_data['lastName']

        response = MyRequests.post("/user/", data=user_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")
        self.id = self.get_json_value(response, "id")
        return self

    def login(self):
        login_data = {
                'email': self.email,
                'password': self.password
        }

        response = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")
        return auth_sid, token

    def __repr__(self):
        return str(self.__dict__)
