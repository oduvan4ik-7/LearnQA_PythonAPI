import requests


def get_auth_cookie(cookie_str):
    cookie_str = cookie_str[cookie_str.index("auth_cookie"):]  # отрезаем лишнее в начале
    # возвращаем значене между "auth_cookie=" и ближайшей ";"
    return cookie_str[:cookie_str.index(";")]



response = requests.post("https://playground.learnqa.ru/api/get_301", allow_redirects=True, data={"p1": "val1"})
# print(response.text)
first_response = response.history[0]
second_response = response
print(response.status_code)
print(first_response, first_response.url)
print(second_response, second_response.url)

print(type(get_auth_cookie(" djhvbjauth_cookie=488959; expires")) , get_auth_cookie(" djhvbjauth_cookie=488959; expires"))