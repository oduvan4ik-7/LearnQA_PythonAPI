import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
history = response.history
for h in history:
    print(h, h.url, h.status_code)
print(response, response.url, response.status_code)
print(f"редиректов: {len(history)}, итоговый URL: {response.url}")
