# Style Presets для Nano Banana

Коллекция готовых пресетов стилей для быстрой генерации изображений.

## Структура

```
style-presets/
├── photorealistic/    # Фотореалистичные изображения
├── artistic/          # Художественные стили
├── professional/      # Профессиональная фотография
├── conceptual/        # Концепт-арт и дизайн
└── custom/            # Пользовательские пресеты
```

## Как использовать пресеты

### Через скрипт

```bash
python3 /opt/ai-workspace/.claude/skills/nano-banana-image-gen/scripts/generate.py \
  --prompt "описание изображения" \
  --style-preset название_пресета
```

### В коде

```python
from generate import generate_image

result = generate_image(
    prompt="mountain landscape",
    style_preset="photorealistic-landscape"
)
```

## Создание своего пресета

1. Создайте файл в соответствующей категории:
   ```
   style-presets/custom/my-style.md
   ```

2. Используйте следующий формат:

```markdown
# Название пресета

Описание пресета

## Template

```
{prompt}, [ваши модификаторы стиля],
[параметры качества], [освещение], [композиция]
```

## Использование

```bash
python3 generate.py --style-preset my-style "описание"
```
```

3. Маркер `{prompt}` будет заменён на фактический промпт пользователя

## Доступные пресеты

### Photorealistic

- `example-portrait` - профессиональные портреты
- *(добавьте свои...)*

### Artistic

- *(пока пусто - создайте свои пресеты!)*

### Professional

- *(пока пусто - создайте свои пресеты!)*

### Conceptual

- *(пока пусто - создайте свои пресеты!)*

### Custom

- *(ваши пользовательские пресеты)*

## Идеи для пресетов

### Фотография
- Landscape photography
- Product photography
- Street photography
- Macro photography
- Architectural photography

### Художественные стили
- Oil painting
- Watercolor
- Digital art
- Anime/Manga style
- Pixel art
- Vector illustration

### Специфические эстетики
- Cyberpunk
- Steampunk
- Fantasy
- Sci-Fi
- Retro/Vintage
- Minimalist

### Профессиональные
- Corporate headshots
- Fashion photography
- Food photography
- Real estate photography

## Примеры шаблонов

### Cyberpunk
```
{prompt}, cyberpunk aesthetic, neon lights,
futuristic cityscape, dark atmospheric mood,
purple and blue color palette, highly detailed,
digital art style, cinematic lighting
```

### Oil Painting
```
{prompt}, oil painting on canvas,
impressionist style, visible brush strokes,
rich warm colors, classical composition,
artistic masterpiece, museum quality
```

### Product Photography
```
{prompt}, professional product photography,
clean white background, studio lighting,
sharp focus, high resolution, commercial quality,
perfect shadows and highlights, 4k
```

## Советы

1. **Используйте описательные имена** файлов:
   - ✅ `cyberpunk-cityscape.md`
   - ❌ `preset1.md`

2. **Тестируйте пресеты** перед использованием

3. **Документируйте** примеры использования

4. **Группируйте** похожие пресеты в категории

5. **Делитесь** удачными пресетами с командой

## Обновление

Чтобы добавить новую категорию:

```bash
mkdir -p /opt/ai-workspace/.claude/skills/nano-banana-image-gen/style-presets/новая-категория
```

Затем создавайте пресеты внутри новой папки.
