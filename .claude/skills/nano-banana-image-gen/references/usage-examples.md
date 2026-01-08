# Примеры использования

## Text-to-Image примеры

### Пример 1: Простая генерация для Telegram (2K)

```bash
# 1. Генерируем изображение
RESULT=$(python3 /opt/ai-workspace/.claude/skills/nano-banana-image-gen/scripts/generate.py \
  "A cute cat sitting on a windowsill, sunny day, photorealistic")

# 2. Отправляем пользователю
/opt/ai-workspace/commands/tg-session-send.sh --file "$RESULT" "Ваше изображение готово!"

# 3. Удаляем временный файл
rm "$RESULT"
```

### Пример 2: Генерация высокого качества (4K)

```bash
# Когда пользователь просит максимальное качество
RESULT=$(python3 /opt/ai-workspace/.claude/skills/nano-banana-image-gen/scripts/generate.py \
  "A cute cat sitting on a windowsill, sunny day, photorealistic" \
  --image-size 4K)

/opt/ai-workspace/commands/tg-session-send.sh --file "$RESULT" "Ваше 4K изображение готово!"
rm "$RESULT"
```

### Пример 3: С улучшением промпта

```bash
# Исходный запрос пользователя: "красивый закат"

# Улучшенный промпт
ENHANCED_PROMPT="A breathtaking sunset over the ocean, \
vibrant orange and pink clouds reflecting on calm water, \
silhouette of palm trees in foreground, \
golden hour lighting, photorealistic, \
cinematic composition, high resolution"

# Генерация
RESULT=$(python3 /opt/ai-workspace/.claude/skills/nano-banana-image-gen/scripts/generate.py \
  "$ENHANCED_PROMPT")

/opt/ai-workspace/commands/tg-session-send.sh --file "$RESULT" "Ваш улучшенный закат готов!"
rm "$RESULT"
```

## Image-to-Image примеры

### Пример 4: Редактирование загруженного изображения

```bash
# Пользователь отправил фото через Telegram
# Оно сохранено в /opt/ai-workspace/.claude/skills/telegram-notifier/uploads/photos/

# Находим последнее загруженное фото
SOURCE_IMAGE=$(ls -t /opt/ai-workspace/.claude/skills/telegram-notifier/uploads/photos/*.jpg | head -1)

# Редактируем по запросу пользователя
RESULT=$(python3 /opt/ai-workspace/.claude/skills/nano-banana-image-gen/scripts/edit.py edit \
  "$SOURCE_IMAGE" \
  "Make it look like a vintage photograph, sepia tones, add film grain" \
  --image-size 2K)

# Отправляем результат
/opt/ai-workspace/commands/tg-session-send.sh --file "$RESULT" "Винтажная версия вашего фото готова!"

# Удаляем временный файл
rm "$RESULT"
```

### Пример 5: Workflow "Создай изображение, затем измени его"

```bash
# Шаг 1: Генерируем базовое изображение
/opt/ai-workspace/commands/tg-send.sh "🎨 Создаю базовое изображение..."

BASE_IMAGE=$(python3 /opt/ai-workspace/.claude/skills/nano-banana-image-gen/scripts/generate.py \
  "A modern office interior, minimalist design, natural lighting, professional photography")

# Шаг 2: Редактируем созданное изображение
/opt/ai-workspace/commands/tg-send.sh "✨ Добавляю детали..."

FINAL_IMAGE=$(python3 /opt/ai-workspace/.claude/skills/nano-banana-image-gen/scripts/edit.py edit \
  "$BASE_IMAGE" \
  "Add plants in the corners, warmer color temperature, make it more cozy" \
  --image-size 2K)

# Отправляем финальный результат
/opt/ai-workspace/commands/tg-session-send.sh --file "$FINAL_IMAGE" \
  "✅ Готово! Создал офис и добавил уютные детали."

# Удаляем временные файлы
rm "$BASE_IMAGE" "$FINAL_IMAGE"
```

### Пример 6: Multi-turn редактирование (серия улучшений)

```bash
# Пользователь: "Создай портрет и сделай его более драматичным"

# Шаг 1: Создаём базовый портрет
/opt/ai-workspace/commands/tg-send.sh "👤 Генерирую базовый портрет..."

BASE=$(python3 /opt/ai-workspace/.claude/skills/nano-banana-image-gen/scripts/generate.py \
  "Professional portrait of a person, neutral background, natural lighting")

# Шаг 2: Применяем серию улучшений
/opt/ai-workspace/commands/tg-send.sh "🎭 Делаю портрет драматичным (3 этапа)..."

FINAL=$(python3 /opt/ai-workspace/.claude/skills/nano-banana-image-gen/scripts/edit.py multi-turn \
  "$BASE" \
  "Darken the background to pure black" \
  "Add dramatic side lighting from the left, creating strong shadows" \
  "Increase contrast and make the mood more intense" \
  --image-size 4K)

# Отправляем результат
/opt/ai-workspace/commands/tg-session-send.sh --file "$FINAL" \
  "✅ Драматичный портрет готов! Применил 3 этапа улучшений."

# Удаляем временные файлы
rm "$BASE" "$FINAL"
```

### Пример 7: Использование референсных изображений

```bash
# Пользователь отправил 2 фото: исходное + референс стиля

# Находим загруженные изображения
UPLOADS_DIR="/opt/ai-workspace/.claude/skills/telegram-notifier/uploads/photos"
SOURCE=$(ls -t $UPLOADS_DIR/*.jpg | head -1)      # Последнее фото
REFERENCE=$(ls -t $UPLOADS_DIR/*.jpg | head -2 | tail -1)  # Предпоследнее

# Применяем стиль референса к исходному изображению
RESULT=$(python3 /opt/ai-workspace/.claude/skills/nano-banana-image-gen/scripts/edit.py edit \
  "$SOURCE" \
  "Apply the artistic style and color palette from the reference image, \
   maintain the composition of the source image" \
  --reference-images "$REFERENCE" \
  --image-size 4K)

/opt/ai-workspace/commands/tg-session-send.sh --file "$RESULT" \
  "✅ Применил стиль референса к вашему изображению!"

rm "$RESULT"
```

### Пример 8: Изменение формата изображения

```bash
# Пользователь: "Переделай фото в формат для Instagram Stories (9:16)"

SOURCE_IMAGE=$(ls -t /opt/ai-workspace/.claude/skills/telegram-notifier/uploads/photos/*.jpg | head -1)

RESULT=$(python3 /opt/ai-workspace/.claude/skills/nano-banana-image-gen/scripts/edit.py edit \
  "$SOURCE_IMAGE" \
  "Extend the image vertically for Instagram Stories format, \
   maintain the style and add appropriate background to fill the space" \
  --aspect-ratio 9:16 \
  --image-size 2K)

/opt/ai-workspace/commands/tg-session-send.sh --file "$RESULT" \
  "✅ Адаптировал под Instagram Stories (9:16)!"

rm "$RESULT"
```

## Workflow для Telegram

1. Получить запрос от пользователя
2. Улучшить промпт (если нужно)
3. Запустить генерацию через скрипт
4. Получить путь к сгенерированному изображению
5. Отправить через `/tg-file`
6. ⚠️ **Временный файл удалять НЕ нужно** - скрипт `tg-session-send.sh` автоматически удаляет файл после отправки
