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

