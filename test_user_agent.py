import json
import pytest
import requests


# python -m pytest -s test_user_agent.py
class TestUserAgent:

    params = [
        {
            'number': "1",
            'agent': 'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
            'expected': {'platform': 'Mobile', 'browser': 'No', 'device': 'Android'}
        },
        {
            'number': "2",
            'agent': 'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
            'expected': {'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'}
        },
        {
            'number': "3",
            'agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'expected': {'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'}
        },
        {
            'number': "4",
            'agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0',
            'expected': {'platform': 'Web', 'browser': 'Chrome', 'device': 'No'}
        },
        {
            'number': "5",
            'agent': 'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'expected': {'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'}
        }
    ]

    @pytest.mark.parametrize('params', params)
    def test_user_agent(self, params):
        headers = {
            'User-Agent': params['agent']}
        expected_platform = params['expected']['platform']
        expected_browser = params['expected']['browser']
        expected_device = params['expected']['device']

        response = requests.get("https://playground.learnqa.ru/ajax/api/user_agent_check", headers=headers)
        try:
            response_json = json.loads(response.text)
        except json.JSONDecodeError:
            print("response is not a json format")

        assert 'platform' in response_json, "There is no attribute 'platform' in the response"
        assert response_json['platform'] == expected_platform, f"Incorrect platform: {response_json['platform']} " \
                                                               f"instead of {expected_platform}, params #{params['number']}"

        assert 'browser' in response_json, "There is no attribute 'browser' in the response"
        assert response_json['browser'] == expected_browser, f"Incorrect browser: {response_json['browser']} " \
                                                             f"instead of {expected_browser}, params #{params['number']}"

        assert 'device' in response_json, "There is no attribute 'device' in the response"
        assert response_json['device'] == expected_device, f"Incorrect device: {response_json['device']} " \
                                                           f"instead of {expected_device}, params #{params['number']}"





