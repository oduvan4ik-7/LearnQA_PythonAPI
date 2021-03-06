import  requests


# python -m pytest -s test_hw_lesson3.py -k phrase
def test_phrase():
    phrase = input("Set a phrase with max len 15 characters: ")
    length = len(phrase)

    assert length <= 15, f"Your phrase has length={length}, which is longer than 15 characters"


# python -m pytest -s test_hw_lesson3.py -k cook
def test_cookie():

    response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
    print(response.cookies)
    #  <RequestsCookieJar[<Cookie HomeWork=hw_value for .playground.learnqa.ru/>]>
    hw_cookie_name_expected = "HomeWork"
    hw_cookie_value_expected = "hw_value"

    assert hw_cookie_name_expected in response.cookies, f"No '{hw_cookie_name_expected}' in cookies"
    hw_cookie_value = response.cookies.get(hw_cookie_name_expected)
    assert hw_cookie_value == hw_cookie_value_expected, f"Cookie_value '{hw_cookie_value}' is not equal to '{hw_cookie_value_expected}'"


# python -m pytest -s test_hw_lesson3.py -k head
def test_header():

    response = requests.get("https://playground.learnqa.ru/api/homework_header")
    print(response.headers)
    # ... 'x-secret-homework-header': 'Some secret value' ...

    hw_header_name_expected = "x-secret-homework-header"
    hw_header_value_expected = "Some secret value"

    assert hw_header_name_expected in response.headers, f"No '{hw_header_name_expected}' in headers"
    hw_header_value = response.headers.get(hw_header_name_expected)
    assert hw_header_value == hw_header_value_expected, f"Header_value '{hw_header_value}' is not equal to '{hw_header_value_expected}'"
