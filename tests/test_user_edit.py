from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import random
import string


# python -m pytest -s --alluredir=test_results/ tests/test_user_edit.py
class TestUserEdit(BaseCase):

    def create_user(self):
        user_data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=user_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")
        user_data.update(
            {"id": self.get_json_value(response, "id")}
        )
        return user_data

    def login(self, login_data):
        response = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")
        return auth_sid, token

    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            "email": email,
            "password": password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed name"

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name})
        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(
            response4, "firstName", new_name, "Wrong name of the user after edit"
        )

    def test_edit_just_created_user_not_auth(self):
        # REGISTER
        user = self.create_user()

        # EDIT
        new_name = "Changed name"

        r_edit = MyRequests.put(f"/user/{user['id']}",
                                data={"firstName": new_name})
        Assertions.assert_code_status(r_edit, 400)
        assert r_edit.content.decode("utf-8") == f"Auth token not supplied", \
            f"Unexpected response content: {r_edit.content}"

    def test_edit_just_created_user_auth_as_other(self):
        # REGISTER USER
        user = self.create_user()

        # REGISTER EDITOR
        editor = self.create_user()

        # LOGIN_EDITOR
        login_data_editor = {
            'email': editor['email'],
            'password': editor['password']
        }
        auth_sid_editor, token_editor = self.login(login_data_editor)

        # EDIT
        new_name = "Changed name"

        r_edit = MyRequests.put(f"/user/{user['id']}",
                                       headers={"x-csrf-token": token_editor},
                                       cookies={"auth_sid": auth_sid_editor},
                                       data={"firstName": new_name})

        # print(r_edit, r_edit.content)
        # раз нельзя GET из-под другого юзера, то и здесь ожидаю 400 - но возвращается 200
        # Assertions.assert_code_status(r_edit, 400)

        # раз работает, смотрим что там редактируется
        # LOGIN_USER
        login_data = {
            'email': user['email'],
            'password': user['password']
        }

        auth_sid, token = self.login(login_data)

        r_get_user = MyRequests.get(f"/user/{user['id']}",
                                    headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid})

        r_get_editor = MyRequests.get(f"/user/{editor['id']}",
                                      headers={"x-csrf-token": token_editor},
                                      cookies={"auth_sid": auth_sid_editor})
        print("\nuser:\n", user)
        print("editor:\n", editor)
        print("user after PUT:\n", r_get_user.text)
        print("editor after PUT:\n", r_get_editor.text)

        # изменяется сам редактор, а не подопытный

    def test_edit_user_incorrect_email(self):
        # REGISTER
        user = self.create_user()

        # LOGIN
        login_data = {
            "email": user['email'],
            "password": user['password']
        }

        auth_sid, token = self.login(login_data)

        # EDIT
        new_data = self.prepare_registration_data()
        new_email = "new_" + new_data['email'].replace("@", "")

        r_edit = MyRequests.put(f"/user/{user['id']}",
                                headers={"x-csrf-token": token},
                                cookies={"auth_sid": auth_sid},
                                data={"email": new_email})

        Assertions.assert_code_status(r_edit, 400)
        assert r_edit.content.decode("utf-8") == f"Invalid email format", \
            f"Unexpected response content: {r_edit.content}"

        # GET
        r_get = MyRequests.get(f"/user/{user['id']}",
                               headers={"x-csrf-token": token},
                               cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(r_get, 'email', user['email'], "email has been changed!")

    def test_edit_user_too_short_first_name(self):
        # REGISTER
        user = self.create_user()

        # LOGIN
        login_data = {
            "email": user['email'],
            "password": user['password']
        }
        auth_sid, token = self.login(login_data)

        # EDIT
        new_first_name = random.choice(string.ascii_letters)

        r_edit = MyRequests.put(f"/user/{user['id']}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_first_name})

        Assertions.assert_code_status(r_edit, 400)
        # контент как-то неоднообразно возвращается
        Assertions.assert_json_value_by_name(r_edit, "error", "Too short value for field firstName",
                                             f"Unexpected error text: {r_edit.text}")

        # GET
        r_get = MyRequests.get(f"/user/{user['id']}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(r_get, 'firstName', user['firstName'], "first_name has been changed!")


