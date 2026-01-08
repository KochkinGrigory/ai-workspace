# Nano Banana API Documentation

## Официальная документация

- **Model ID:** `gemini-3-pro-image-preview`
- **Provider:** Google Generative AI (Gemini)
- **API Endpoint:** Через `google-genai` Python SDK
- **Официальный гайд:** https://ai.google.dev/gemini-api/docs/image-generation

## Установка зависимостей

```bash
pip install google-genai
```

## API Ключ

API ключ хранится в переменной окружения:

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

Или в файле `/opt/ai-workspace/.env`:

```
GEMINI_API_KEY=YOUR_API_KEY
```

## Базовое использование

```python
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

model = "gemini-3-pro-image-preview"
contents = [
    types.Content(
        role="user",
        parts=[
            types.Part.from_text(text="Your prompt here"),
        ],
    ),
]

generate_content_config = types.GenerateContentConfig(
    response_modalities=["IMAGE", "TEXT"],
    image_config=types.ImageConfig(
        image_size="2K",  # или "1K", "4K"
    ),
)

for chunk in client.models.generate_content_stream(
    model=model,
    contents=contents,
    config=generate_content_config,
):
    # Process chunks...
    pass
```

## Конфигурация

### Response Modalities

Определяет формат ответа:

```python
response_modalities=["IMAGE", "TEXT"]
```

- `IMAGE` - модель будет возвращать изображения
- `TEXT` - модель может возвращать текстовые описания

### Image Size / Quality

Определяет разрешение и качество изображения:

```python
image_config=types.ImageConfig(
    image_size="2K",  # Опции: "1K", "2K", "4K"
)
```

- `1K` - быстрая генерация, базовое качество
- `2K` - баланс качества и скорости (рекомендуется по умолчанию)
- `4K` - максимальное качество, медленнее

### Inline Data

Изображения возвращаются через `inline_data`:

```python
inline_data = chunk.candidates[0].content.parts[0].inline_data
data_buffer = inline_data.data
mime_type = inline_data.mime_type
```

## Форматы изображений

Обычно возвращается **PNG** формат:
- MIME type: `image/png`
- Расширение: `.png`

## Rate Limiting

Официальные лимиты зависят от тарифного плана Google AI.

**Рекомендации:**
- Добавьте задержку между запросами (~1-2 секунды)
- Обрабатывайте ошибки 429 (Too Many Requests)
- Используйте exponential backoff при повторных попытках

## Обработка ошибок

```python
try:
    for chunk in client.models.generate_content_stream(...):
        # Process
        pass
except Exception as e:
    if "quota" in str(e).lower():
        print("Quota exceeded")
    elif "invalid" in str(e).lower():
        print("Invalid request")
    else:
        print(f"Unknown error: {e}")
```

## Цены (приблизительные)

- **Официальный API Google:** ~$0.134 - $0.24 за изображение
- **Сторонние провайдеры:** от $0.05 за изображение

Актуальные цены смотрите на:
- [Google AI Pricing](https://ai.google.dev/pricing)
- [Third-party providers](https://nanobananaapi.ai/)

## Ограничения

1. **Контент:**
   - Запрещён NSFW контент
   - Запрещены изображения известных людей без контекста
   - Запрещено насилие

2. **Технические:**
   - Максимальная длина промпта: ~2000 символов (рекомендуется)
   - Максимальное количество запросов: зависит от тарифа

3. **Качество:**
   - Модель может неправильно интерпретировать сложные промпты
   - Детали могут быть неточными (особенно текст на изображениях)

## Безопасность

- **НЕ** коммитьте API ключ в Git
- Храните ключ в `.env` файле
- Используйте переменные окружения
- Регулярно ротируйте ключи

## Полезные ссылки

- [Google AI Studio](https://aistudio.google.com/)
- [Google Generative AI SDK](https://pypi.org/project/google-genai/)
- [Official Documentation](https://ai.google.dev/docs)
