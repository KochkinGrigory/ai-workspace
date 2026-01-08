# Методология "Пять столпов" (Five Pillars)

> **🔑 Ключевой принцип v1.5.1:** Nano Banana Pro использует **Reasoning Engine**, а не статистическое распознавание ключевых слов как старые диффузионные модели.

## От тегов к сценариям

**Что изменилось:**

Gemini 3 Pro Image Preview (Nano Banana Pro) фундаментально отличается от моделей типа Stable Diffusion или DALL-E 2. Это не "рисование по ключевым словам", а **симуляция реальной съемки/создания контента**.

**❌ Старый подход (теги):**
```
cat, sunset, beach, photorealistic, 4k, professional
```

**✅ Новый подход (сценарий):**
```
A ginger tabby cat sitting on wet sand at the ocean's edge during sunset,
watching the waves roll in. The cat's fur catches the warm golden light
from the setting sun. Shot with Canon EOS R5 using 85mm f/1.8 lens at f/2.8,
creating soft bokeh in the background where orange and pink clouds reflect
on the water surface. Natural beach lighting with strong backlight creating
rim light around the cat's silhouette. Photorealistic, sharp focus on cat's
eyes with visible whisker detail and individual fur strands.
```

**Почему это работает:**
- Модель понимает **контекст и отношения** между элементами
- Обрабатывает **физику света** и материалов
- Создает **связную сцену**, а не коллаж тегов
- Генерирует **правдоподобные детали** на основе логики

---

## Архитектура "Пять столпов"

Каждый промпт должен структурироваться по пяти основным компонентам:

### 1️⃣ Субъект (Subject)
**Что изображено:** Детальное описание главного объекта.

**Обязательно указать:**
- Физические характеристики (возраст, пол, материал, размер)
- Эмоции и выражение (для людей/персонажей)
- Одежда/покрытие/отделка
- Уникальные особенности

**Примеры:**
- Портрет: "confident business executive, male in his mid-40s with salt-and-pepper hair, wearing navy blue suit"
- Продукт: "premium wireless headphones, matte black finish with rose gold accents, over-ear design"
- Объект: "vintage leather armchair, cognac brown color, tufted backrest, brass nailhead trim"

---

### 2️⃣ Действие (Action)
**Что происходит:** Динамика, движение, физика.

**Обязательно указать:**
- Что делает субъект
- Напряжение мышц, поза
- Взаимодействие с окружением
- Физика (ветер, гравитация, инерция)

**Примеры:**
- Портрет: "making direct eye contact with camera, displaying warm yet authoritative smile"
- Продукт: "headphones resting on wooden surface with headband slightly compressed, showing cushion softness"
- Действие: "athlete mid-jump, legs tucked, arms extended, hair flowing upward from momentum"

---

### 3️⃣ Окружение (Location/Context)
**Где это происходит:** Место, атмосфера, контекст освещения.

**Обязательно указать:**
- Физическое расположение
- Время суток / погодные условия
- Атмосфера и настроение
- Источники света (естественные и искусственные)

**Примеры:**
- Интерьер: "modern corporate office with neutral gray seamless background, subtle gradient lighting"
- Природа: "mountain lake at sunset with mirror-like water reflections, pine trees along shoreline"
- Студия: "professional photo studio with white cyclorama background, controlled lighting setup"

---

### 4️⃣ Композиция/Камера (Composition/Camera)
**Как снято:** Технические параметры съемки.

**Обязательно указать:**
- Тип камеры (для фотореализма)
- Фокусное расстояние (35mm, 50mm, 85mm, 100mm macro, 135mm)
- Диафрагма (f/1.2, f/2.8, f/5.6, f/11) → глубина резкости
- Угол съемки, кадрирование
- Зона фокуса

**Примеры фокусных расстояний:**
- 35mm - широкий угол, контекст
- 50mm - естественная перспектива
- 85mm - портретный стандарт (золотой стандарт для лиц)
- 100mm macro - детали, текстуры, продукты
- 135mm - телефото, компрессия перспективы

**Примеры диафрагмы:**
- f/1.2 - f/2.0: экстремально малая ГРИП, сильное боке
- f/2.8 - f/4: портреты, отделение от фона
- f/5.6 - f/8: групповые портреты, продукты
- f/11 - f/16: пейзажи, резкость от переднего до заднего плана

**Примеры:**
- "Shot on Hasselblad H6D with 80mm f/2.8 lens at f/4 for optimal sharpness across face"
- "Canon EOS R5 using 100mm macro lens at f/8 for full product sharpness, no depth blur"
- "35mm wide angle at f/11 capturing entire landscape in sharp focus from foreground to background"

---

### 5️⃣ Стиль (Style)
**Визуальная эстетика:** Художественный язык, постобработка.

**Обязательно указать:**
- Жанр (editorial, commercial, artistic, documentary)
- Эстетический язык (minimalist, dramatic, vintage, modern)
- Постобработка (color grading, retouching level)
- Целевое использование (magazine, social media, billboard)
- Разрешение и качество

**Примеры:**
- "Editorial corporate photography for Fortune 500 annual report, minimal retouching, professional color grading with slight cool tone, 8K resolution"
- "Commercial product photography for e-commerce, clean white background, true-to-life colors, web-optimized"
- "Fine art landscape photography, dramatic HDR processing, saturated colors, gallery print quality"

---

## Полный пример: Применение всех 5 столпов

**Запрос пользователя:** "профессиональное фото бизнесмена"

**❌ Плохой промпт (старый подход):**
```
businessman, professional, suit, office, 4k, high quality
```

**✅ Хороший промпт (5 столпов):**
```
1. СУБЪЕКТ:
Professional business executive, male in his mid-40s with salt-and-pepper hair
neatly styled, confident authoritative presence. Wearing impeccably tailored
charcoal gray three-piece suit with crisp white shirt and burgundy silk tie.

2. ДЕЙСТВИЕ:
Making direct eye contact with camera, displaying warm yet authoritative smile.
Arms crossed confidently, shoulders squared, relaxed but commanding posture.

3. ОКРУЖЕНИЕ:
Shot in modern corporate office environment with floor-to-ceiling windows showing
city skyline softly blurred in background. Natural daylight from large windows
mixing with subtle artificial fill light. Clean professional atmosphere.

4. КОМПОЗИЦИЯ/КАМЕРА:
Shot on Hasselblad H6D medium format camera with 80mm f/2.8 lens, aperture set
to f/4 for optimal sharpness across entire face while creating gentle background
separation. Classic headshot framing from mid-chest up, centered composition with
head room following rule of thirds.

5. СТИЛЬ:
Editorial corporate photography for Fortune 500 annual report. Classic three-point
studio lighting - large octagonal softbox as key light from 45 degrees creating
gentle modeling, fill light opposite opening shadows, subtle rim light for
separation. Minimal retouching maintaining natural character lines and skin
texture. Professional color grading with slight cool tone emphasizing authority.
8K resolution for print quality.
```

**Результат:** Модель создаст связную сцену с правильным освещением, реалистичной кожей, корректной глубиной резкости и профессиональной композицией.

---

## Адаптация "5 столпов" к разным контекстам

Базовая структура остается, но акценты меняются:

**Фотография портретов** → акцент на текстуры кожи, эмоции, освещение лица
**Фотография продуктов** → акцент на материалы, студийный свет, чистота фона
**Инфографика** → акцент на структуру информации, типографику, layout logic
**Презентации** → акцент на negative space, читаемость текста, title-safe зоны

**Детальные адаптации см. в:**
- [photography-portraits.md](../best-practices/photography-portraits.md) - "Фотореализм через текстуры"
- [photography-products.md](../best-practices/photography-products.md) - "Виртуальная Студия"
- [design-infographics.md](../best-practices/design-infographics.md) - "Structure-First Design"
- [business-presentations.md](../best-practices/business-presentations.md) - "Negative Space First"

---

## Текстуры и фотореализм (критично для портретов)

**Проблема:** AI часто создает "пластиковую кожу" без реализма.

**Решение:** Явно описывать **взаимодействие света с материалом**.

**Обязательные ключевые слова для кожи:**
- `visible skin pores` - видимые поры
- `freckles` - веснушки (если уместно)
- `vellus hair` / `peach fuzz` - пушковые волосы
- `subsurface scattering` - подповерхностное рассеивание света
- `minor imperfections` - мелкие несовершенства
- `catchlight in eyes` - блик в глазах
- `individual hair strands` - отдельные волоски

**Пример:**
```
Close-up portrait with natural skin texture clearly visible - pores defined,
subtle freckles across nose, vellus hair (peach fuzz) catching light along
cheekbones, subsurface scattering showing warm undertones where light passes
through ears and nose, catchlight in eyes from softbox, minor imperfections
maintaining photorealistic character rather than retouched perfection.
```

---

## Negative Prompts (отрицательные промпты)

Nano Banana Pro поддерживает указание нежелательных элементов.

**Типовые для всех промптов:**
```
Negative Prompt: cartoon, illustration, anime, drawing, painting,
3D render, CGI, artificial, plastic skin, overly smooth, bad quality,
deformed, distorted, watermark, text overlay, signature
```

**Для портретов добавить:**
```
airbrushed skin, retouched, plastic appearance, doll-like,
unrealistic smoothness, fake
```

**Для продуктов добавить:**
```
cluttered background, distracting elements, poor lighting,
shadows obscuring product, reflections hiding details
```
