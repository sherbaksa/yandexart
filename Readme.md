# YandexART - AI Image Generator

<div align="center">

![YandexART](https://img.shields.io/badge/YandexART-AI%20Generator-00ffff?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0.0-black?style=for-the-badge&logo=flask)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Современный веб-интерфейс для генерации изображений с помощью Yandex Art API**

[Демо](#возможности) • [Установка](#установка) • [Использование](#использование) • [API](#api-endpoints)

</div>

---

## Описание

**YandexART** — это веб-приложение на Flask с футуристическим интерфейсом для генерации изображений с использованием Yandex Art API. Проект позволяет создавать уникальные логотипы и изображения на основе текстовых описаний в различных стилях.

### Возможности

- Генерация изображений по текстовому описанию
- Множество стилей: фотореализм, аниме, киберпанк, акварель и другие
- Быстрая генерация с автоматическим ожиданием результата
- Автоматическое сохранение сгенерированных изображений
- Современный UI с неоновыми эффектами и анимациями
- Адаптивный дизайн для всех устройств
- Автоматическое обновление IAM-токена каждый час

---

## Технологии

### Backend
- **Flask 3.0.0** - веб-фреймворк
- **Python 3.8+** - язык программирования
- **Requests** - HTTP-клиент для работы с Yandex API
- **python-dotenv** - управление переменными окружения

### Frontend
- **HTML5/CSS3** - структура и стилизация
- **JavaScript (ES6+)** - клиентская логика
- **Bootstrap 5.3.0** - адаптивная сетка
- **Google Fonts** (Orbitron, Rajdhani) - типографика

### API
- **Yandex Art API** - генерация изображений
- **Yandex IAM API** - аутентификация

---

## Установка

### Предварительные требования

- Python 3.8 или выше
- pip (менеджер пакетов Python)
- Аккаунт Yandex Cloud с активированным сервисом Yandex Art

### Шаг 1: Клонирование репозитория

```bash
git clone https://github.com/sherbaksa/yandexart.git
cd yandexart
```

### Шаг 2: Создание виртуального окружения

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Шаг 3: Установка зависимостей

```bash
pip install -r requests.txt
```

### Шаг 4: Настройка переменных окружения

1. Скопируйте файл `.env.example`:
```bash
cp .env.example .env
```

2. Откройте `.env` и заполните ваши данные:
```env
OAUTH_TOKEN="your_yandex_oauth_token_here"
CATALOG_ID="your_yandex_catalog_id_here"
```

#### Как получить учетные данные:

**OAuth Token:**
1. Перейдите на [Yandex OAuth](https://oauth.yandex.ru/)
2. Создайте новое приложение
3. Получите OAuth-токен

**Catalog ID:**
1. Войдите в [Yandex Cloud Console](https://console.cloud.yandex.ru/)
2. Выберите ваш каталог
3. Скопируйте ID каталога из URL или настроек

---

## Использование

### Запуск приложения

```bash
python app.py
```

Приложение будет доступно по адресу: **http://localhost:5002**

### Генерация изображения

1. Откройте веб-интерфейс в браузере
2. Введите **стиль изображения** (например: "Киберпанк", "Аниме", "Фотореализм")
3. Введите **описание** желаемого изображения
4. Нажмите кнопку **"ГЕНЕРИРОВАТЬ"**
5. Дождитесь завершения генерации (обычно 30-60 секунд)
6. Скачайте готовое изображение

### Примеры промптов

```
Стиль: Киберпанк
Описание: Футуристический город с неоновыми огнями и летающими машинами

Стиль: Аниме
Описание: Девушка с розовыми волосами на фоне цветущей сакуры

Стиль: Фотореализм
Описание: Космонавт на поверхности Марса смотрит на закат
```

---

## API Endpoints

### `GET /`
Главная страница приложения

**Ответ:** HTML-страница с интерфейсом

---

### `POST /generate`
Генерация изображения

**Запрос:**
```json
{
  "style": "Киберпанк",
  "description": "Футуристический город"
}
```

**Успешный ответ (200):**
```json
{
  "success": true,
  "image_url": "/generated/image_20241029_143022.jpg"
}
```

**Ошибка (400/500):**
```json
{
  "success": false,
  "error": "Описание ошибки"
}
```

---

### `GET /static/generated/<filename>`
Получение сгенерированного изображения

**Пример:** `/static/generated/image_20241029_143022.jpg`

---

## Структура проекта

```
YandexART/
├── app.py                    # Главный файл Flask-приложения
├── image_generator.py        # Модуль генерации изображений
├── requests.txt              # Зависимости проекта
├── .env                      # Переменные окружения (не в Git)
├── .env.example              # Пример переменных окружения
├── .gitignore               # Игнорируемые файлы
├── static/
│   ├── css/
│   │   └── style.css        # Стили интерфейса
│   ├── js/
│   │   └── main.js          # Клиентская логика
│   └── generated/           # Папка для сохранения изображений
├── templates/
│   └── index.html           # HTML-шаблон главной страницы
└── venv/                    # Виртуальное окружение (не в Git)
```

---

## Конфигурация

### Настройка сервера

По умолчанию приложение запускается на:
- **Host:** `0.0.0.0` (доступен из сети)
- **Port:** `5002`
- **Debug:** `True` (отключите в production)

Для изменения параметров отредактируйте `app.py`:

```python
if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000)
```

### Настройка генерации

В файле `image_generator.py` можно настроить:
- **Aspect Ratio** - соотношение сторон изображения
- **Seed** - случайное значение для генерации
- **Max Attempts** - максимальное количество попыток проверки статуса

---

## Безопасность

**Важно:**
- Никогда не публикуйте файл `.env` в Git
- Храните OAuth-токен в безопасности
- В production используйте `debug=False`
- Рекомендуется использовать HTTPS для production
- Регулярно обновляйте зависимости

---

## Решение проблем

### Ошибка: "Не удалось получить IAM-токен"
- Проверьте правильность `OAUTH_TOKEN` в `.env`
- Убедитесь, что токен не истек

### Ошибка: "Не удалось сгенерировать изображение"
- Проверьте `CATALOG_ID` в `.env`
- Убедитесь, что сервис Yandex Art активирован
- Проверьте лимиты вашего аккаунта

### Изображение не отображается
- Проверьте права на папку `static/generated/`
- Убедитесь, что путь к файлу корректный

---

## Лицензия

Этот проект распространяется под лицензией MIT. Подробности в файле [LICENSE](LICENSE).

---

## Автор

Создано для работы с Yandex Art API

---

## Вклад в проект

Вклад в проект приветствуется! Если вы хотите улучшить проект:

1. Сделайте Fork репозитория
2. Создайте ветку для новой функции (`git checkout -b feature/AmazingFeature`)
3. Сделайте Commit изменений (`git commit -m 'Add some AmazingFeature'`)
4. Отправьте изменения в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

---

## Поддержка

Если у вас возникли вопросы или проблемы:

- [Создайте Issue](https://github.com/sherbaksa/yandexart/issues)
- Напишите на email: sherbaksa@gmail.com
- [Документация Yandex Art](https://cloud.yandex.ru/docs/foundation-models/concepts/yandexart)

---

## Благодарности

- [Yandex Cloud](https://cloud.yandex.ru/) за предоставление API
- [Flask](https://flask.palletsprojects.com/) за отличный фреймворк
- [Bootstrap](https://getbootstrap.com/) за адаптивную сетку

---

<div align="center">

**Если проект вам понравился, поставьте звезду на GitHub!**

Made with Yandex Art API

</div>