import datetime
import os
from definitions import ROOT_DIR
from requests import Response


class Logger:
    # при запуске из интерфейса pycharm рабочая директория - tests (os.getcwd())
    file_name = f"{os.path.join(ROOT_DIR)}/logs/log_" + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + ".log"

    @classmethod
    def _write_log_to_file(cls, data: str):
        # 'a' Opens a file for appending at the end of the file without truncating it.
        # Creates a new file if it does not exist.
        try:
            with open(cls.file_name, 'a', encoding='utf-8') as logger_file:
                logger_file.write(data)
        except FileNotFoundError:
            print(f"something wrong with file {cls.file_name}")

    @classmethod
    def add_request(cls, url: str, data: dict, headers: dict, cookies: dict, method: str):
        testname = os.environ.get('PYTEST_CURRENT_TEST')
        data_to_add = f"\n-----\n"
        data_to_add += f"Test: {testname}\n"
        data_to_add += f"Time: {str(datetime.datetime.now())}\n"
        data_to_add += f"Request method: {method}\n"
        data_to_add += f"Request url: {url}\n"
        data_to_add += f"Request data: {data}\n"
        data_to_add += f"Request headers: {headers}\n"
        data_to_add += f"Request cookies: {cookies}\n"
        data_to_add += "\n"

        cls._write_log_to_file(data_to_add)

    @classmethod
    def add_response(cls, response: Response):
        cookies_as_dict = dict(response.cookies)
        headers_as_dict = dict(response.headers)

        data_to_add = f"Response code: {response.status_code}\n"
        data_to_add += f"Response text: {response.text}\n"
        data_to_add += f"Response headers: {headers_as_dict}\n"
        data_to_add += f"Response cookies: {cookies_as_dict}\n"
        data_to_add += f"\n-----\n"

        cls._write_log_to_file(data_to_add)








