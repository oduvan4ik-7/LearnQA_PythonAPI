import requests

url_compare_types = "https://playground.learnqa.ru/ajax/api/compare_query_type"

response = requests.get(url_compare_types)
print("1. Запрос без параметра method:", response, response.text)

response = requests.head(url_compare_types, data={'method': "HEAD"})
print("2. Запрос не из списка (HEAD):", response, response.text)

response = requests.post(url_compare_types, data={'method': "POST"})
print("3. Запрос с правильным 'method' (POST):", response, response.text)

types = ['GET', 'POST', 'PUT', 'DELETE']  # , 'HEAD', 'PATCH' - всегда 400
# i = 1
for real_type in types:
    for type_in_param in types:
        if real_type == 'GET':
            r = requests.request(url=url_compare_types, method=real_type, params={'method': type_in_param})
        else:
            r = requests.request(url=url_compare_types, method=real_type, data={'method': type_in_param})

        if (real_type == type_in_param) != (r.text == '{"success":"!"}'):
            print(f"4. Несоответствие! выполнен метод {real_type}, с параметром method={type_in_param}, результат: {r.text} ")

        # print(i, real_type.ljust(6), type_in_param.ljust(6),  r, r.text, )
        # i += 1



