import string
import random

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import pytest


class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content: {response.content}"

    def test_create_user_with_incorrect_email(self):
        data = self.prepare_registration_data()
        data['email'] = data['email'].replace("@", "")

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", \
            f"Unexpected response content: {response.content}"

    fields = ['password', 'username', 'firstName', 'lastName', 'email']

    @pytest.mark.parametrize("field", fields)
    def test_create_user_with_missing_field(self, field):
        data = self.prepare_registration_data()
        data[field] = None

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {field}", \
            f"Unexpected response content: {response.content}"

    def test_create_user_with_too_short_first_name(self):
        data = self.prepare_registration_data()
        data['firstName'] = random.choice(string.ascii_letters)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too short", \
            f"Unexpected response content: {response.content}"

    def test_create_user_with_too_long_first_name(self):
        max_len = 250
        data = self.prepare_registration_data()
        data['firstName'] = "".join([random.choice(string.ascii_letters) for i in range(max_len+1)])

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too long", \
            f"Unexpected response content: {response.content}"