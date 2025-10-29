import requests
import random
import time
import base64
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

OAUTH_TOKEN = os.getenv("OAUTH_TOKEN")
CATALOG_ID = os.getenv("CATALOG_ID")

# Глобальные переменные для IAM-токена
iam_token = None
token_expires_at = None


def get_iam_token():
    """Получение IAM-токена через OAuth-токен"""
    url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
    headers = {"Content-Type": "application/json"}
    data = {"yandexPassportOauthToken": OAUTH_TOKEN}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        token_data = response.json()
        print(f"IAM-токен успешно получен в {datetime.now().strftime('%H:%M:%S')}")
        return token_data['iamToken']
    else:
        raise Exception(f"Ошибка получения IAM-токена: {response.status_code} - {response.text}")


def refresh_token_if_needed():
    """Обновление токена если прошел час или токен не получен"""
    global iam_token, token_expires_at

    current_time = datetime.now()

    if iam_token is None or token_expires_at is None or current_time >= token_expires_at:
        iam_token = get_iam_token()
        token_expires_at = current_time + timedelta(hours=1)
        print(f"Следующее обновление токена в {token_expires_at.strftime('%H:%M:%S')}")

    return iam_token


def generate_image_from_prompt(style, description):
    """
    Генерация изображения на основе стиля и описания

    Args:
        style (str): Стиль изображения (например: "Фотореализм", "Аниме", "Акварель")
        description (str): Краткое описание изображения

    Returns:
        str: Путь к сохраненному файлу или None в случае ошибки
    """
    # Формируем полный промпт
    prompt = f"Сгенерируй логотип по описанию {description} и обязательно в стиле {style}. Генерируемое изображение обязательно должно быть логотипом! И соответствовать описанию {description}"

    # Получаем актуальный IAM-токен
    current_iam_token = refresh_token_if_needed()

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync"
    headers = {
        "Authorization": f"Bearer {current_iam_token}",
        "Content-Type": "application/json"
    }
    data = {
        "modelUri": f"art://{CATALOG_ID}/yandex-art/latest",
        "generationOptions": {
            "seed": f"{random.randint(0, 1000000)}",
            "aspectRatio": {
                "widthRatio": "1",
                "heightRatio": "1"
            }
        },
        "messages": [
            {
                "text": prompt
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        request_id = response.json()['id']
        print(f"Запрос отправлен. ID операции: {request_id}")
        print("Ожидание генерации изображения...")

        max_attempts = 100
        attempt = 0

        while attempt < max_attempts:
            time.sleep(3)
            attempt += 1

            current_iam_token = refresh_token_if_needed()
            headers["Authorization"] = f"Bearer {current_iam_token}"

            status_url = f"https://llm.api.cloud.yandex.net:443/operations/{request_id}"
            response = requests.get(status_url, headers=headers)

            if response.status_code == 200:
                result = response.json()

                if result.get('done', False):
                    if 'response' in result and 'image' in result['response']:
                        image_base64 = result['response']['image']
                        image_data = base64.b64decode(image_base64)

                        # Создаем папку для изображений если её нет
                        os.makedirs("static/generated", exist_ok=True)

                        filename = f"static/generated/image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                        with open(filename, "wb") as f:
                            f.write(image_data)
                        print(f"Изображение успешно сохранено как {filename}")
                        return filename
                    elif 'error' in result:
                        print(f"Ошибка при генерации: {result['error']}")
                        return None
                else:
                    print(f"Попытка {attempt}: операция еще выполняется...")
            else:
                print(f"Ошибка при проверке статуса: {response.status_code} - {response.text}")
                return None

        print("Превышено максимальное время ожидания")
        return None
    else:
        print(f"Ошибка при отправке запроса: {response.text}")
        return None