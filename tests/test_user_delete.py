from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from model.user import User


# python -m pytest -s --alluredir=test_results/ tests/test_user_delete.py
class TestUserDelete(BaseCase):

    def test_delete_user_with_id_2(self):
        user = User()

        user.email = 'vinkotov@example.com'
        user.password = '1234'

        auth_sid, token = user.login()

        r_delete = MyRequests.delete(f"/user/2",
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(r_delete, 400)
        assert r_delete.content.decode("utf-8") == f"Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response content: {r_delete.content}"

    def test_delete_user(self):
        user = User()
        user.create()

        auth_sid, token = user.login()

        r_delete = MyRequests.delete(f"/user/{user.id}",
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(r_delete, 200)

        r_get = MyRequests.get(f"/user/{user.id}",
                               headers={"x-csrf-token": token},
                               cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(r_get, 404)
        assert r_get.content.decode("utf-8") == f"User not found", \
            f"Unexpected response content: {r_get.content}"

    def test_delete_user_auth_as_other(self):
        editor = User()
        editor.create()

        user = User()
        user.create()

        auth_sid_editor, token_editor = editor.login()

        r_delete = MyRequests.delete(f"/user/{user.id}",
                                     headers={"x-csrf-token": token_editor},
                                     cookies={"auth_sid": auth_sid_editor})

        print(r_delete, r_delete.content)
        # Assertions.assert_code_status(r_delete, 400)

        r_get_editor = MyRequests.get(f"/user/{editor.id}",
                                      headers={"x-csrf-token": token_editor},
                                      cookies={"auth_sid": auth_sid_editor})

        print(r_get_editor, r_get_editor.content)
        # Assertions.assert_code_status(r_get_editor, 200)
        # удалился сам удаляльщик
