import requests
import json


class CloudflareAPI:
    def __init__(self, api_tok, account_id):
        self.api_tok = "33-EOtC6ik09mzjjgi2Lck5H84kfLr4PSW1fa3Px"  # Сохраняем API ключ
        self.account_id = account_id  # Сохраняем email для аутентификации
        self.base_url =  "https://api.cloudflare.com/client/v4/accounts/890a7d87e18704d8b94c46045099d984/ai/run/@cf/meta/llama-3.3-70b-instruct-fp8-fast" # Базовый URL для API Cloudflare

    def generate_solution(self, task_text):
        """
        Отправляет текст задачи в LLM через Cloudflare и возвращает решение.
        :param task_text: Текст задачи, который нужно обработать LLM
        :return: Ответ от LLM
        """
        headers = {
            "Authorization": f"Bearer {self.api_tok}",  # Заголовок авторизации
            "Content-Type": "application/json"  # Указываем, что отправляем JSON
        }
        data = {
            "prompt": task_text,
            "max_tokens": 200,
            "temperature": 0.7,
            "top_p": 0.9
        }

        try:
            # Отправляем POST запрос в Cloudflare
            response = requests.post(self.base_url, headers=headers, json=data)

            response.raise_for_status()  # Вызываем исключение для HTTP ошибок

            response_json = response.json()

            # Проверяем структуру ответа и извлекаем текст
            if "result" in response_json and "response" in response_json["result"]:
                return response_json["result"]["response"]
            else:
                print(f"Unexpected response format: {response_json}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")  # Печатаем ошибку
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
