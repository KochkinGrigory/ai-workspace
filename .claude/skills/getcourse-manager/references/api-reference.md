# GetCourse API Reference

> Подробная техническая документация по GetCourse REST API

## Базовая информация

### Базовый URL
```
https://{account_name}.getcourse.ru/pl/api/{endpoint}
```

### Протокол
- Только **HTTPS** (SSL обязателен)
- HTTP запросы будут отклонены

### Формат запроса
```http
POST /pl/api/{endpoint}
Content-Type: application/x-www-form-urlencoded

action={action}&key={secret_key}&params={base64_json}
```

### Формат ответа
```json
{
  "success": "true",
  "action": "add",
  "result": {
    "success": "true",
    "user_id": "12345",
    "error": "false"
  }
}
```

---

## Аутентификация

### Секретный ключ (API Key)

**Получение:**
1. Войти в админку GetCourse
2. Настройки → API
3. Сгенерировать секретный ключ

**Использование:**
```
key={secret_key}
```

Передается в каждом запросе как POST параметр.

**Безопасность:**
- Не передавать в GET параметрах (только POST body)
- Не коммитить в репозиторий
- Хранить в `.env` файле
- Использовать только HTTPS

---

## Основные эндпоинты

### 1. Пользователи (Users)

**Endpoint:** `/pl/api/users`

**Действия:**
- `add` - добавить/обновить пользователя
- `update` - обновить существующего

#### Добавление пользователя

**Action:** `add`

**Минимальные параметры:**
```json
{
  "user": {
    "email": "user@example.com"
  }
}
```

ИЛИ

```json
{
  "user": {
    "phone": "+79001234567"
  }
}
```

**Полные параметры:**
```json
{
  "user": {
    "email": "ivan@example.com",
    "phone": "+79001234567",
    "first_name": "Иван",
    "last_name": "Петров",
    "middle_name": "Сергеевич",
    "city": "Москва",
    "country": "Россия",
    "birthday": "01.01.1990",
    "group_name": ["Группа1", "Группа2"],
    "addfields": {
      "Telegram": "@ivan",
      "Источник": "VK реклама",
      "Промокод": "SUMMER2024"
    }
  },
  "system": {
    "refresh_if_exists": 1,
    "partner_email": "partner@example.com"
  },
  "session": {
    "utm_source": "vk",
    "utm_medium": "cpc",
    "utm_campaign": "summer",
    "utm_content": "ad1",
    "utm_term": "keyword",
    "referer": "https://vk.com/page"
  }
}
```

**Ответ:**
```json
{
  "success": "true",
  "action": "add",
  "result": {
    "success": "true",
    "user_id": "123456",
    "user_status": "active",
    "error": "false"
  }
}
```

#### Обновление групп пользователя

**Action:** `update`

**Параметры:**
```json
{
  "user_id": "123456",
  "group_name": ["Новая группа 1", "Новая группа 2"]
}
```

**⚠️ Важно:** При обновлении групп передается ПОЛНЫЙ список. Группы не в списке будут удалены.

---

### 2. Заказы (Deals)

**Endpoint:** `/pl/api/deals`

**Действия:**
- `add` - создать заказ
- `update` - обновить заказ

#### Создание заказа

**Action:** `add`

**Минимальные параметры:**

Вариант 1 (по коду оффера):
```json
{
  "user": {
    "email": "user@example.com"
  },
  "deal": {
    "offer_code": "COURSE2024",
    "deal_cost": "9990"
  }
}
```

Вариант 2 (по ID оффера):
```json
{
  "user": {
    "email": "user@example.com"
  },
  "deal": {
    "offer_id": 12345
  }
}
```

**Полные параметры:**
```json
{
  "user": {
    "email": "user@example.com",
    "phone": "+79001234567",
    "first_name": "Иван",
    "last_name": "Петров"
  },
  "deal": {
    "deal_number": "ORD-2024-001",
    "offer_code": "TRAINING2024",
    "product_title": "Курс SMM",
    "quantity": 1,
    "deal_cost": "9990",
    "deal_currency": "RUB",
    "deal_is_paid": "1",
    "payment_type": "card",
    "payment_status": "accepted",
    "manager_email": "manager@example.com",
    "comment": "Оплата по безналу"
  }
}
```

**Статусы заказа (deal_status):**
- `new` - новый
- `in_work` - в работе
- `payment_waiting` - ожидание оплаты
- `payed` - оплачен
- `part_payed` - частично оплачен
- `cancelled` - отменен

**Статусы оплаты (payment_status):**
- `expected` - ожидается
- `accepted` - принята
- `returned` - возвращена
- `tobalance` - на баланс
- `frombalance` - с баланса

**Типы оплаты (payment_type):**
- `card` - банковская карта
- `bank` - банковский перевод
- `paypal` - PayPal
- `yandex` - Яндекс.Касса
- `webmoney` - WebMoney
- `cash` - наличные

**Ответ:**
```json
{
  "success": "true",
  "action": "add",
  "result": {
    "success": "true",
    "deal_id": "789012",
    "user_id": "123456",
    "error": "false"
  }
}
```

---

### 3. Группы (Groups)

**Endpoint:** `/pl/api/account/groups`

#### Получение списка групп

**Метод:** GET

**Параметры:**
```
?key={secret_key}
```

**URL:**
```
https://{account_name}.getcourse.ru/pl/api/account/groups?key={secret_key}
```

**Ответ:**
```json
{
  "success": "true",
  "result": {
    "groups": [
      {
        "id": 1,
        "title": "Тренинг SMM",
        "users_count": 150,
        "description": "Основная группа курса SMM"
      },
      {
        "id": 2,
        "title": "VIP Студенты",
        "users_count": 25,
        "description": "Премиум доступ"
      }
    ]
  }
}
```

#### Получение пользователей группы

**Endpoint:** `/pl/api/account/groups/{group_id}/users`

**URL:**
```
https://{account_name}.getcourse.ru/pl/api/account/groups/123/users?key={secret_key}
```

---

### 4. Сообщения (Messages)

**Endpoint:** `/pl/api/messages`

#### Отправка сообщения

**Action:** `send`

**Параметры:**
```json
{
  "message": {
    "email": "user@example.com",
    "transport": "email",
    "mailing_id": "5",
    "params": {
      "first_name": "Иван",
      "custom_field": "значение"
    }
  }
}
```

**Транспорты (transport):**
- `email` - электронная почта
- `sms` - SMS сообщение
- `telegram` - Telegram

---

## Export API

### Общие принципы

Export API работает в два этапа:
1. **Инициация экспорта** - отправка запроса на формирование выгрузки
2. **Проверка статуса и скачивание** - получение готовой выгрузки

### Лимиты
- **100 запросов** за 2 часа
- Доступно только на платных тарифах

### Экспорт пользователей

**Endpoint:** `/pl/api/account/export`

**Параметры:**
```json
{
  "object": "users",
  "filter": {
    "created_at_from": "2024-01-01",
    "created_at_to": "2024-12-31",
    "group_id": 123,
    "status": "active"
  }
}
```

---

## Обработка ошибок

### Формат ошибки

```json
{
  "success": "false",
  "error": "true",
  "error_message": "Invalid API key"
}
```

### Типичные ошибки

| Код | Сообщение | Причина |
|-----|-----------|---------|
| 400 | Invalid key | Неверный API ключ |
| 400 | Email or phone required | Не указан email или телефон |
| 400 | User already exists | Пользователь существует (нужен refresh_if_exists) |
| 400 | Offer not found | Оффер с таким кодом не найден |
| 403 | Access denied | Нет доступа к API (Trial тариф) |
| 404 | Group not found | Группа не найдена |
| 429 | Rate limit exceeded | Превышен лимит запросов |
| 500 | Internal server error | Ошибка сервера GetCourse |

### Обработка ошибок в коде

```python
result = api_call()

# Проверка успешности
if result.get("success") == "true":
    print("Успех!")
    user_id = result["result"]["user_id"]
else:
    # Обработка ошибки
    error_msg = result.get("error_message", "Unknown error")
    print(f"Ошибка: {error_msg}")
```

---

## Лимиты и ограничения

### По тарифам

| Тариф | Import API | Export API | Лимит объектов/месяц |
|-------|------------|------------|----------------------|
| Trial | ❌ Нет | ❌ Нет | - |
| Start | ✅ Да | ✅ Да | 1,000 |
| Business | ✅ Да | ✅ Да | 10,000 |
| Professional | ✅ Да | ✅ Да | Без лимита |

### Rate Limits

- **Import:** Зависит от тарифа (обычно 100-500 запросов/час)
- **Export:** 100 запросов за 2 часа
- **Рекомендация:** Пауза 1 секунда между запросами

---

## Best Practices

### 1. Используйте refresh_if_exists

```json
{
  "system": {
    "refresh_if_exists": 1
  }
}
```

Позволяет избежать ошибок при повторном добавлении.

### 2. Проверяйте существование групп

```bash
# Сначала получите список групп
curl "https://account.getcourse.ru/pl/api/account/groups?key=KEY"

# Используйте точное название
```

### 3. Логируйте все операции

```python
import logging

logging.info(f"Adding user: {email}")
result = add_user(email)
logging.info(f"Result: {result}")
```

### 4. Обрабатывайте таймауты

```python
import requests

try:
    response = requests.post(url, data=data, timeout=30)
except requests.exceptions.Timeout:
    print("Request timed out")
```

### 5. Используйте retry для временных ошибок

```python
from tenacity import retry, stop_after_attempt, wait_fixed

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def add_user_with_retry(email):
    return add_user(email)
```

---

## Примеры на разных языках

### Python

```python
import requests
import base64
import json

def add_user(email):
    params = {
        "user": {"email": email},
        "system": {"refresh_if_exists": 1}
    }

    params_b64 = base64.b64encode(
        json.dumps(params).encode()
    ).decode()

    data = {
        "action": "add",
        "key": API_KEY,
        "params": params_b64
    }

    response = requests.post(API_URL, data=data)
    return response.json()
```

### JavaScript (Node.js)

```javascript
const axios = require('axios');

async function addUser(email) {
  const params = {
    user: { email },
    system: { refresh_if_exists: 1 }
  };

  const paramsB64 = Buffer.from(
    JSON.stringify(params)
  ).toString('base64');

  const data = new URLSearchParams({
    action: 'add',
    key: API_KEY,
    params: paramsB64
  });

  const response = await axios.post(API_URL, data);
  return response.data;
}
```

### cURL

```bash
# Подготовка параметров
PARAMS='{"user":{"email":"user@example.com"},"system":{"refresh_if_exists":1}}'
PARAMS_B64=$(echo -n "$PARAMS" | base64)

# Запрос
curl -X POST "https://account.getcourse.ru/pl/api/users" \
  -d "action=add" \
  -d "key=$API_KEY" \
  -d "params=$PARAMS_B64"
```

---

## Дополнительные ресурсы

**Официальная документация:**
- https://getcourse.ru/help/api - основная документация
- https://getcourse.ru/blog/276212 - статья про API

**GitHub репозитории:**
- https://github.com/getcourse-ru/GetCourse-PHP-SDK - PHP SDK

**Поддержка:**
- Email: support@getcourse.ru
- Чат в админке GetCourse
