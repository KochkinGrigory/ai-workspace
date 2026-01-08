# Troubleshooting

## Ошибка: "API key not found"

**Проблема:** Переменная окружения `GEMINI_API_KEY` не установлена.

**Решение:**
```bash
# Добавьте в /opt/ai-workspace/.env
echo 'GEMINI_API_KEY=ваш_ключ_из_google_ai_studio' >> /opt/ai-workspace/.env
```

Скрипты генерации и редактирования **автоматически загружают** конфигурацию из `.env` при запуске.

---

## Ошибка: "Rate limit exceeded"

**Проблема:** Превышен лимит запросов к API.

**Решение:**
- Подождите несколько минут между запросами
- Обновите тарифный план Google AI Studio
- Проверьте квоты: https://aistudio.google.com/

---

## Ошибка: "User location is not supported for the API use"

**Проблема:** Google API блокирует VPS серверы, даже если они находятся в поддерживаемых регионах.

**Решение:** Настройте прокси-сервер.

### Быстрое решение с прокси

```bash
# Добавьте в /opt/ai-workspace/.env
HTTP_PROXY=http://username:password@proxy-host:port
HTTPS_PROXY=http://username:password@proxy-host:port
```

**Пример:**
```bash
# /opt/ai-workspace/.env
GEMINI_API_KEY=AIzaSyC...abc123
HTTP_PROXY=http://user:pass@proxy.example.com:8080
HTTPS_PROXY=http://user:pass@proxy.example.com:8080
```

**Как это работает:**
- При импорте скрипты (`generate.py`, `edit.py`) автоматически вызывают функцию `load_env_file()`
- Функция читает `/opt/ai-workspace/.env` и загружает все переменные
- Если `HTTP_PROXY` и `HTTPS_PROXY` установлены, все запросы к Google API идут через прокси
- Логирование: в stderr выводится `[INFO] Using proxy for requests`
- Переменные, уже установленные в окружении, имеют приоритет (не перезаписываются)

**Работа без прокси:**
```bash
# Просто закомментируйте или удалите строки прокси в .env
# HTTP_PROXY=...
# HTTPS_PROXY=...

# Запросы пойдут напрямую (может не работать на VPS)
```

**Ручная настройка (опционально):**
Если вы хотите переопределить настройки из .env для конкретного запуска:
```bash
export HTTP_PROXY=http://other-proxy:port
python3 generate.py "..."
```

---

## Низкое качество изображения

**Проблема:** Сгенерированное изображение выглядит нечетко или недостаточно детализировано.

**Решения:**

### 1. Используйте 4K качество
```bash
# Добавьте флаг --image-size 4K
python3 generate.py "промпт" --image-size 4K
```

### 2. Улучшите промпт
- **Используйте повествовательное описание** вместо списка слов
- **Применяйте методологию "5 столпов":** субъект, действие, окружение, камера, стиль
- См. [five-pillars-methodology.md](five-pillars-methodology.md)

**Плохо:**
```
cat, sunset, beach, photorealistic
```

**Хорошо:**
```
A ginger tabby cat sitting on wet sand at ocean's edge during sunset,
watching waves roll in. Cat's fur catches warm golden light from setting sun.
Shot with Canon EOS R5 using 85mm f/1.8 lens at f/2.8, creating soft bokeh.
Photorealistic, sharp focus on cat's eyes with visible whisker detail.
```

### 3. Добавьте технические детали

**Для портретов:**
- Тип камеры: "Shot on Hasselblad H6D"
- Объектив: "80mm f/2.8 lens at f/4"
- Текстуры кожи: "visible skin pores, natural texture"
- Освещение: "studio lighting, softbox from 45 degrees"

**Для продуктов:**
- Объектив: "100mm macro lens at f/8"
- Фон: "white cyclorama background"
- Освещение: "professional product photography lighting"

### 4. Уточните стиль
- `photorealistic`, `realistic photography`
- `cinematic lighting`, `dramatic composition`
- `professional quality`, `8k resolution`
- `high detail`, `sharp focus`

### 5. Опишите освещение
- `natural light`, `golden hour`, `sunset lighting`
- `studio lighting`, `three-point lighting`
- `rim lighting`, `dramatic shadows`
- `soft diffused light`, `volumetric lighting`

---

## Изображение выглядит "пластиковым" (искусственным)

**Проблема:** Особенно для портретов - кожа выглядит неестественно гладкой.

**Решение:** Явно описывайте текстуры и несовершенства.

**Обязательные ключевые слова для реалистичной кожи:**
```
visible skin pores, natural skin texture, freckles,
vellus hair (peach fuzz), subsurface scattering,
minor imperfections, catchlight in eyes,
individual hair strands, realistic
```

**Пример:**
```
Close-up portrait with natural skin texture clearly visible - pores defined,
subtle freckles across nose, vellus hair catching light along cheekbones,
subsurface scattering showing warm undertones, catchlight in eyes,
minor imperfections maintaining photorealistic character
rather than retouched perfection.
```

См. подробнее: [photography-portraits.md](../best-practices/photography-portraits.md)

---

## Персонажи не консистентны в серии изображений

**Проблема:** При создании нескольких изображений одного персонажа, он выглядит по-разному.

**Решение:** Используйте первое изображение как референс для остальных.

**Workflow:**
```bash
# 1. Первое БЕЗ референса
python3 generate.py "Detailed prompt for character"
# → photo_1.jpg

# 2. Остальные С РЕФЕРЕНСОМ на первое
python3 generate.py "Same person from reference, different pose" \
  --reference-images photo_1.jpg

python3 generate.py "Same person from reference, another angle" \
  --reference-images photo_1.jpg
```

**Важно в промпте:**
- "Same person/character from reference image"
- "Maintain facial features from reference"
- "Keep consistent appearance with reference"

См. подробнее: [character-consistency.md](character-consistency.md)

---

## Текст на изображении на английском вместо русского

**Проблема:** Для русскоязычной аудитории генерируется текст на английском.

**Решение:** Явно указывайте язык и шрифт в промпте.

**Дефолтные настройки для РФ:**
```
All text in Russian language,
use Manrope font for all text elements,
clean modern typography
```

**Пример:**
```bash
python3 generate.py "Create an infographic with title 'Наши достижения 2024',
use Manrope font for all text, all labels in Russian,
clean modern design"
```

См. также: раздел "Дефолтные настройки для русской аудитории" в SKILL.md

---

## Логотип бренда не используется

**Проблема:** При запросе "добавь логотип Фонда" он не находится или не применяется.

**Решение:** Проверьте наличие логотипа в brands storage и используйте его как reference image.

```bash
# 1. Проверить наличие
ls brands/фонд/assets/logos/

# 2. Использовать как референс
python3 generate.py "Presentation slide for Fond" \
  --reference-images brands/фонд/assets/logos/fond_logo_default.png
```

**Текущие бренды и логотипы:**
- Фонд: `brands/фонд/assets/logos/fond_logo_default.png`
- Люкс Оптика: `brands/люкс-оптика/assets/logos/lux_optics_logo.png`
- Ангелы Зрения: `brands/ангелы-зрения/assets/logos/angels_logo_main.png`
- Оптика Будущего: `brands/оптика-будущего/assets/logos/optics_future_logo.png`

См. подробнее: [brand-assets-guide.md](brand-assets-guide.md)

---

## Скрипт не находит .env файл

**Проблема:** Переменные окружения не загружаются из `.env`.

**Решение:** Убедитесь, что файл находится по пути `/opt/ai-workspace/.env`:

```bash
# Проверить наличие
ls -la /opt/ai-workspace/.env

# Если нет - создать
touch /opt/ai-workspace/.env
chmod 600 /opt/ai-workspace/.env

# Добавить ключ API
echo 'GEMINI_API_KEY=ваш_ключ' >> /opt/ai-workspace/.env
```

Скрипты автоматически ищут `.env` в `/opt/ai-workspace/.env` и загружают переменные при импорте.
