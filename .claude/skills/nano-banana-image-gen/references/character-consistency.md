# Консистентность персонажей в сериях изображений

**ВАЖНОЕ ПРАВИЛО:** При создании серии изображений с одним персонажем, объектом или моделью используй первое изображение как референс для остальных.

## Когда применять

Пользователь просит создать **несколько изображений** где должен быть:
- Один и тот же человек/персонаж
- Один и тот же объект/продукт
- Фотосессия модели
- Серия рекламных материалов

**Триггеры:**
- "Сделай фотосессию из 3 снимков"
- "Создай серию изображений с персонажем"
- "Несколько фото одного человека в разных позах"
- "3 варианта баннера с одной моделью"

## Workflow для консистентности

```bash
# 1. Генерация первого изображения (БЕЗ референсов)
python3 generate.py "Detailed prompt for first photo" --image-size 4K
# → photo_1.jpg

# 2. Генерация остальных С РЕФЕРЕНСОМ на первое
python3 generate.py "Second photo with same person, different pose" \
  --reference-images photo_1.jpg \
  --image-size 4K

python3 generate.py "Third photo with same person, another angle" \
  --reference-images photo_1.jpg \
  --image-size 4K
```

## Пример реализации

**Запрос пользователя:**
> "Сделай фотосессию из 3 снимков девушки в очках в парке"

**Правильная последовательность Claude:**

**Шаг 1:** Генерация первого БЕЗ референсов
```python
generate.py "Woman wearing eyeglasses in park, low angle shot..." --image-size 4K
→ photo_1.jpg
```

**Шаг 2:** Второе С РЕФЕРЕНСОМ на первое
```python
generate.py "Same woman from reference image, dynamic spin movement,
maintaining same facial features and style from reference..." \
  --reference-images photo_1.jpg \
  --image-size 4K
→ photo_2.jpg  # Та же девушка
```

**Шаг 3:** Третье С РЕФЕРЕНСОМ на первое
```python
generate.py "Same woman from reference image, lying on grass,
keep consistent appearance with reference..." \
  --reference-images photo_1.jpg \
  --image-size 4K
→ photo_3.jpg  # Та же девушка
```

## Преимущества

✅ **Консистентность лица** - один и тот же человек во всех снимках
✅ **Единство стиля** - сохраняется визуальный язык
✅ **Профессиональный результат** - как настоящая фотосессия
✅ **Брендовая согласованность** - для маркетинговых материалов

## Важные детали промпта

При генерации 2+ изображений с референсом ОБЯЗАТЕЛЬНО указывать:
- "Same person/character from reference image"
- "Maintain facial features from reference"
- "Keep consistent appearance with reference"

**Пример промпта для 2-го изображения:**
```
Same woman from reference image wearing eyeglasses, now sitting on park bench,
casual outfit, maintain same facial features and hairstyle from reference,
different pose but same person, natural park lighting, photorealistic
```
