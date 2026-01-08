# Nano Banana Prompting Guide v2.0

> **Версия:** 2.0 (Обновлено для методологии "Пять столпов")
> **Модель:** Gemini 3 Pro Image Preview (Nano Banana Pro)
> **Источники:** [Официальный гайд Google](https://ai.google.dev/gemini-api/docs/image-generation?hl=ru#prompt-guide) + Архитектура промпт-инжиниринга Nano Banana Pro

---

## Ключевой принцип v2.0

### 🧠 Reasoning Engine vs Tag-Based Models

**Gemini 3 Pro Image Preview (Nano Banana Pro)** использует фундаментально другую архитектуру по сравнению с диффузионными моделями (Stable Diffusion, DALL-E 2):

**Старые модели (Stable Diffusion, Midjourney):**
- Статистическое распознавание ключевых слов
- "Рисование по тегам"
- Результат = коллаж элементов с высокой корреляцией к тегам

**Nano Banana Pro (Gemini 3 Pro Image Preview):**
- **Reasoning Engine** - семантическое понимание сцены
- Симуляция реальной съемки/создания контента
- Результат = связная сцена с физикой света и материалов

---

### От тегов к сценариям

**❌ Старый подход (теги):**
```
cat, sunset, beach, photorealistic, 4k, professional
```
**Проблема:** Модель "склеивает" разрозненные элементы без понимания контекста.

**✅ Новый подход (сценарий):**
```
A ginger tabby cat sitting on wet sand at the ocean's edge during sunset,
watching the waves roll in. The cat's fur catches the warm golden light
from the setting sun, creating a glowing rim light effect around its silhouette.
Shot with Canon EOS R5 using 85mm f/1.8 lens at f/2.8, creating soft bokeh
in the background where orange and pink clouds reflect on the calm water surface.
Natural beach lighting with strong backlight. Photorealistic, sharp focus
on cat's eyes with visible whisker detail and individual fur strands clearly defined.

Negative Prompt: cartoon, illustration, flat colors, artificial, bad quality
```

**Почему это работает:**
- Модель понимает **взаимосвязи** между элементами (кот → песок → закат)
- Обрабатывает **физику света** (rim light от заката, отражения на воде)
- Симулирует **реальную камеру** (85mm f/2.8 → конкретная глубина резкости)
- Создает **связную композицию**, а не коллаж

---

## Методология "Пять столпов" (Five Pillars)

Каждый промпт для Nano Banana Pro должен структурироваться по **пяти основным компонентам**:

```
1. СУБЪЕКТ (Subject)      - Что изображено
2. ДЕЙСТВИЕ (Action)       - Что происходит
3. ОКРУЖЕНИЕ (Location)    - Где находится, контекст освещения
4. КОМПОЗИЦИЯ (Camera)     - Как снято (камера, оптика, кадрирование)
5. СТИЛЬ (Style)          - Визуальная эстетика, постобработка
```

---

### 1️⃣ Субъект (Subject)

**Что изображено:** Детальное описание главного объекта.

**Обязательно указать:**
- Физические характеристики (возраст, пол, материал, размер, цвет)
- Эмоции и выражение лица (для людей/персонажей)
- Одежда / покрытие / отделка / текстура
- Уникальные особенности и детали

**Примеры:**

**Для портретов:**
```
Confident business executive, male in his mid-40s with salt-and-pepper hair
neatly styled, professional demeanor. Wearing impeccably tailored navy blue
three-piece suit with crisp white shirt and burgundy silk tie.
```

**Для продуктов:**
```
Premium wireless over-ear headphones, matte black finish with rose gold
metallic accents on hinges and logo. Soft memory foam ear cushions in
charcoal gray, adjustable padded headband, modern minimalist design.
```

**Для объектов:**
```
Vintage leather Chesterfield armchair, rich cognac brown color with deep
button-tufted backrest, rolled arms with antique brass nailhead trim,
worn patina showing natural aging and character.
```

---

### 2️⃣ Действие (Action)

**Что происходит:** Динамика, движение, физика, поза.

**Обязательно указать:**
- Что делает субъект (действие или состояние)
- Напряжение мышц, поза, положение тела
- Взаимодействие с окружением
- Физика процесса (гравитация, инерция, ветер, брызги)

**Примеры:**

**Для портретов:**
```
Making direct eye contact with camera, displaying warm yet authoritative smile.
Arms crossed confidently across chest, shoulders squared, spine straight,
relaxed but commanding posture conveying executive presence.
```

**Для продуктов:**
```
Headphones resting on polished wooden surface with headband slightly compressed,
showing the softness and flexibility of the cushioning. Cable naturally coiled
beside the device, creating organic composition.
```

**Для действия:**
```
Professional athlete mid-jump during basketball dunk, legs tucked beneath body,
right arm fully extended upward gripping ball, left arm sweeping back for
balance, jersey rippling from momentum, hair flowing upward from rapid motion.
```

---

### 3️⃣ Окружение (Location/Context)

**Где это происходит:** Место, атмосфера, контекст освещения.

**Обязательно указать:**
- Физическое расположение (интерьер / экстерьер / студия)
- Время суток и погодные условия
- Атмосфера и настроение сцены
- Источники света (естественные и искусственные)
- Фоновые элементы, глубина сцены

**Примеры:**

**Интерьер:**
```
Shot in modern corporate office environment with floor-to-ceiling windows
showing city skyline softly blurred in background. Natural daylight from
large windows mixing with subtle artificial fill light. Clean professional
atmosphere with neutral gray tones, minimal distractions.
```

**Природа:**
```
Mountain lake at sunset with mirror-like water reflections showing perfect
symmetry of snow-capped peaks. Pine trees lining the rocky shoreline creating
natural framing. Dramatic sky with layers of orange, pink, and purple clouds
illuminated by setting sun below horizon.
```

**Студия:**
```
Professional photo studio with white seamless cyclorama background creating
infinite backdrop. Controlled lighting setup - large octagonal softbox as
key light from camera left at 45 degrees, white reflector on right for fill,
rim light from behind for subject separation.
```

---

### 4️⃣ Композиция/Камера (Composition/Camera)

**Как снято:** Технические параметры съемки.

**Обязательно указать:**
- Тип камеры (для фотореализма)
- Фокусное расстояние объектива
- Диафрагма (глубина резкости)
- Угол съемки и кадрирование
- Зона фокуса

#### Фокусные расстояния и их применение

| Фокусное | Назначение | Эффект перспективы | Типичное использование |
|----------|------------|-------------------|------------------------|
| **35mm** | Wide angle | Расширяет пространство, показывает контекст | Пейзажи, интерьеры, групповые фото |
| **50mm** | Standard | Естественная перспектива, как видит глаз | Универсальная съемка, стрит-фото |
| **85mm** | Portrait | Легкая компрессия, лестная перспектива | **Золотой стандарт портретов** |
| **100mm** | Macro | Минимальная дистанция фокусировки | Детали, текстуры, продукты |
| **135mm** | Telephoto | Сильная компрессия фона | Изоляция субъекта, спорт |

#### Диафрагма и глубина резкости

| Диафрагма | Глубина резкости | Боке | Назначение |
|-----------|------------------|------|------------|
| **f/1.2 - f/2.0** | Экстремально малая | Сильное кремовое боке | Портреты с максимальным размытием фона |
| **f/2.8 - f/4** | Средняя | Умеренное боке | Портреты с отделением от фона, сохранение контекста |
| **f/5.6 - f/8** | Средняя-большая | Минимальное боке | Групповые портреты, продукты (полная резкость объекта) |
| **f/11 - f/16** | Максимальная | Нет боке | Пейзажи (резкость от переднего до заднего плана) |

**Примеры:**

**Портрет:**
```
Shot on Hasselblad H6D medium format camera with 80mm f/2.8 lens,
aperture set to f/4 for optimal sharpness across entire face while
creating gentle background separation. Classic headshot framing from
mid-chest up, centered composition with proper head room following
rule of thirds. Sharp focus on eyes, gradient fall-off to ears.
```

**Продукт:**
```
Canon EOS R5 using 100mm macro lens at f/8 for complete front-to-back
sharpness across entire product, no depth blur. Camera positioned at
slight angle (3/4 view) to show both front face and side profile.
Overhead positioning with 15-degree tilt-down angle.
```

**Пейзаж:**
```
35mm wide angle lens at f/11 capturing entire landscape in sharp focus
from foreground rocks to distant mountain peaks. Low camera position
(ground level) emphasizing foreground interest. Centered composition
with horizon line following rule of thirds (upper third).
```

---

### 5️⃣ Стиль (Style)

**Визуальная эстетика:** Художественный язык, постобработка.

**Обязательно указать:**
- Жанр фотографии или искусства
- Эстетический язык
- Уровень постобработки
- Целевое использование
- Разрешение и техническое качество

**Примеры:**

**Editorial Photography:**
```
Editorial corporate photography for Fortune 500 annual report. Classic
three-point studio lighting creating gentle face modeling. Minimal retouching
maintaining natural character lines and skin texture showing professional
maturity. Professional color grading with slight cool tone (blue-gray bias)
emphasizing authority and trustworthiness. 8K resolution for large format print.
```

**Commercial Product:**
```
Commercial product photography for premium e-commerce listing. Clean white
background (255,255,255 RGB), no shadows, perfect color accuracy for online
shopping. Slight contrast boost to make product pop. Web-optimized resolution
with natural true-to-life colors, no artistic color grading.
```

**Fine Art:**
```
Fine art landscape photography in Ansel Adams tradition. Dramatic black and
white conversion with deep blacks and bright highlights. Zone system approach
to tonal range. Gallery print quality with rich texture detail. Timeless
classic aesthetic emphasizing form and light over color.
```

---

## Полные примеры: Применение всех 5 столпов

### Пример 1: Профессиональный портрет

**Запрос пользователя:** "профессиональное фото для LinkedIn"

**Промпт (все 5 столпов):**
```
1. СУБЪЕКТ:
Professional business executive, male in his mid-40s with salt-and-pepper hair
neatly styled, confident authoritative presence. Wearing impeccably tailored
charcoal gray three-piece suit with crisp white shirt and burgundy silk tie.
Natural smile lines visible around eyes showing experience and warmth.

2. ДЕЙСТВИЕ:
Making direct eye contact with camera, displaying warm yet professional smile
showing genuine approachability. Arms crossed confidently across chest,
shoulders squared, relaxed but commanding executive posture.

3. ОКРУЖЕНИЕ:
Shot in modern corporate office environment with floor-to-ceiling windows
showing city skyline softly blurred in background. Natural daylight streaming
from large windows creating soft ambient light. Clean neutral gray backdrop
with minimal visual distractions maintaining professional focus.

4. КОМПОЗИЦИЯ/КАМЕРА:
Shot on Hasselblad H6D medium format camera with 80mm f/2.8 lens, aperture
set to f/4 for optimal sharpness across entire face while creating gentle
bokeh background separation. Classic corporate headshot framing from mid-chest
up, centered composition with proper head room. Sharp focus on eyes with
gradient fall-off maintaining natural depth.

5. СТИЛЬ:
Editorial corporate photography for Fortune 500 annual report or LinkedIn
executive profile. Classic three-point studio lighting - large octagonal
softbox as key light from 45 degrees creating gentle modeling on face,
fill light opposite opening shadows without flattening, subtle rim light
from behind for separation from background. Minimal retouching maintaining
natural skin texture with visible pores and character lines showing
professional maturity. Professional color grading with slight cool tone
emphasizing authority. 8K resolution for print quality.

Negative Prompt: cartoon, illustration, overly retouched, plastic skin,
artificial smoothness, bad quality, deformed features
```

---

### Пример 2: Продуктная фотография

**Запрос:** "снимок наушников для интернет-магазина"

**Промпт:**
```
1. СУБЪЕКТ:
Premium wireless over-ear headphones, matte black finish with rose gold
metallic accents on hinges and brand logo. Soft memory foam ear cushions
in charcoal gray fabric, padded adjustable headband with subtle stitching
detail. Modern minimalist industrial design with clean geometric lines.

2. ДЕЙСТВИЕ:
Headphones positioned in classic 3/4 view resting on polished walnut wooden
surface, headband slightly compressed showing cushion softness and flexibility.
Ear cups angled to display both front face and side profile simultaneously.
Fabric-braided cable naturally coiled beside device creating organic
visual flow.

3. ОКРУЖЕНИЕ:
Professional photo studio with pure white seamless cyclorama background
creating infinite backdrop with no visible edges or shadows. Controlled
lighting environment eliminating any color contamination. Clean minimalist
setting focusing 100% attention on product.

4. КОМПОЗИЦИЯ/КАМЕРА:
Shot on Canon EOS R5 using 100mm macro lens at f/8 for complete front-to-back
sharpness across entire product with no depth blur. Camera positioned at
slight overhead angle with 15-degree downward tilt. Product occupies central
60% of frame with generous white space for clean e-commerce presentation.
Perfect focus across all product surfaces.

5. СТИЛЬ:
Commercial product photography for premium e-commerce listing. Studio lighting
setup: large octagonal softbox from front-left creating even illumination,
white reflector on right filling shadows and preventing harsh contrast, subtle
rim light from behind separating product from background and highlighting edges.
Clean white background (255,255,255 RGB). True-to-life color accuracy critical
for online shopping decisions. Slight contrast boost making product pop without
distorting colors. Web-optimized 4K resolution.

Negative Prompt: cluttered background, distracting elements, shadows obscuring
product, reflections hiding details, incorrect colors, bad lighting
```

---

### Пример 3: Природный пейзаж

**Запрос:** "красивый горный пейзаж на закате"

**Промпт:**
```
1. СУБЪЕКТ:
Dramatic snow-capped mountain range with sharp granite peaks catching last
rays of golden sunset light. Pristine alpine lake in foreground with perfectly
still water creating mirror-like reflections of peaks and colorful sky.
Ancient pine forest lining rocky shoreline creating natural dark framing.

2. ДЕЙСТВИЕ:
Completely still serene moment just after sunset during blue hour transition.
Lake surface absolutely calm without ripples, creating perfect symmetrical
reflections. Subtle mist beginning to form over water surface adding depth
and atmosphere layers.

3. ОКРУЖЕНИЕ:
High alpine wilderness location at approximately 2500 meters elevation during
late summer season. Shot 15 minutes after sunset during magical blue hour
when sky displays gradient from warm orange near horizon through pink and
purple to deep blue overhead. Natural ambient light from residual sunset glow,
no artificial light sources. Clean mountain air providing exceptional clarity
and visibility of distant peaks.

4. КОМПОЗИЦИЯ/КАМЕРА:
Shot on Sony A7R IV with 24mm wide-angle lens at f/11 for maximum depth of
field capturing everything in sharp focus from foreground rocks to distant
peaks. Camera positioned low (50cm above ground) emphasizing foreground rocks
and lake reflections. Horizontal landscape orientation. Composition following
rule of thirds with horizon line placed at lower third, allowing dramatic sky
to dominate upper two-thirds. Central peak aligned with vertical center line
creating symmetrical balanced composition. Foreground rocks providing leading
lines drawing eye toward mountain.

5. СТИЛЬ:
Fine art landscape photography in tradition of Galen Rowell and Ansel Adams.
Rich saturated colors emphasizing natural drama of sunset light - deep oranges,
vibrant pinks, rich purples in clouds contrasting with cool blue shadows.
HDR-style processing bringing out detail in both highlights and shadows without
appearing artificial. Slightly increased clarity and vibrance making landscape
pop. Sharp corner-to-corner focus. Gallery-worthy print quality at 8K resolution.
Timeless nature photography aesthetic.

Negative Prompt: people, buildings, modern structures, artificial elements,
oversaturated, cartoonish, painted look, unrealistic colors
```

---

## Специализированные техники

### Текстуры и фотореализм (для портретов)

**Проблема:** AI часто создает "пластиковую кожу" без реалистичной текстуры.

**Решение:** Явно описывать **взаимодействие света с материалом кожи**.

**Обязательные ключевые слова:**
```
- visible skin pores (видимые поры)
- freckles (веснушки, если уместно)
- vellus hair / peach fuzz (пушковые волосы)
- subsurface scattering (подповерхностное рассеивание света)
- minor imperfections (мелкие несовершенства)
- natural skin texture (естественная текстура кожи)
- catchlight in eyes (блик в глазах от источника света)
- individual hair strands (отдельные волоски)
```

**Пример:**
```
Close-up portrait showing natural photorealistic skin texture - pores clearly
defined across nose and cheeks, subtle freckles scattered across bridge of nose,
fine vellus hair (peach fuzz) visible catching light along cheekbones and jawline.
Subsurface scattering effect showing warm skin undertones where light passes
through translucent areas of ears and nose tip. Prominent catchlight in eyes
from octagonal softbox creating life and dimension. Minor skin imperfections
like small moles and natural character lines maintaining photorealistic
authenticity rather than airbrushed perfection. Individual eyebrow hairs and
eyelashes clearly visible.
```

---

### Negative Prompts (отрицательные промпты)

Nano Banana Pro поддерживает указание **нежелательных элементов** через Negative Prompt.

**Базовый шаблон для всех промптов:**
```
Negative Prompt: cartoon, illustration, anime, drawing, painting, sketch,
3D render, CGI, artificial, plastic appearance, overly smooth skin,
airbrushed, bad quality, low resolution, deformed, distorted anatomy,
watermark, text overlay, signature, logo
```

**Для портретов добавить:**
```
retouched skin, doll-like, plastic face, unrealistic smoothness,
fake appearance, overprocessed, beauty filter
```

**Для продуктов добавить:**
```
cluttered background, distracting elements, poor lighting, harsh shadows,
reflections obscuring product, color inaccuracy, blurry details
```

**Для пейзажей добавить:**
```
people, buildings, modern structures, cars, artificial elements,
power lines, oversaturated, cartoonish colors, unrealistic
```

---

### Генерация текста в изображениях

Nano Banana Pro имеет **уникальную способность** генерировать читаемый текст.

**Правило:** Указывайте ТОЧНЫЙ текст в кавычках.

**Пример (инфографика):**
```
Modern business infographic slide design, 16:9 landscape format.

Title text at top: 'THE FUTURE OF REMOTE WORK'
Subtitle below: 'How COVID-19 permanently changed workplace dynamics'

Left column heading: 'Productivity Metrics'
Body text: 'Teams working remotely reported 23% higher output compared to
traditional office environment, measured across 500 companies.'

Right column heading: 'Cost Savings'
Large statistic: '$11,000' with small label underneath: 'Average annual
savings per employee'

Clean sans-serif typography (Inter or Montserrat style), navy blue headings,
charcoal gray body text, white background with subtle light blue accent shapes,
professional minimalist design.
```

**Пример (презентация):**
```
Title slide background for business presentation, 16:9 landscape.
Professional abstract blue gradient background from navy (#001F3F) at top
fading to lighter blue (#0074D9) at bottom.

Large centered text area (empty negative space) spanning 60% of width × 50%
of height in exact center for title overlay. Geometric abstract shapes
confined to edges - subtle white transparent circles in upper right corner,
thin diagonal lines in lower left, creating modern professional frame without
interfering with text zone.

Text to appear: 'ANNUAL STRATEGY REVIEW 2025'
```

---

### Световые схемы

#### Portrait Lighting Setups

**Rembrandt Lighting:**
```
Classic Rembrandt lighting setup - key light positioned 45 degrees to side
and 45 degrees above subject creating characteristic triangle of light on
shadowed cheek. Small inverted triangle beneath eye on shadow side. Dramatic
mood with distinct separation between highlight and shadow sides of face.
Fill light minimal, allowing shadows to remain deep.
```

**Softbox Studio:**
```
Large octagonal softbox positioned at 45 degrees from subject creating soft
flattering light wrapping around facial features. White reflector on opposite
side bouncing light to gently fill shadows without eliminating dimension.
Subtle rim light from behind separating subject from background. Professional
editorial quality even lighting.
```

**Golden Hour Natural:**
```
Shot during golden hour - 30 minutes before sunset. Subject positioned with
warm low-angle sunlight as backlight creating glowing rim light around hair
and shoulders. Large white reflector in front bouncing golden light back onto
face for soft warm fill. Natural outdoor lighting with warm color temperature
(3500K). Organic beautiful glow.
```

---

## Управление качеством

### Параметр image_size в API

| Параметр | Разрешение | Время генерации | Применение |
|----------|------------|-----------------|------------|
| **1K** | ~1024x1024 | Быстро (~10-15 сек) | Превью, черновики, тесты |
| **2K** | ~2048x2048 | Средне (~20-30 сек) | **Рекомендуется** - баланс качества/скорости |
| **4K** | ~4096x4096 | Медленно (~40-60 сек) | Финальные версии, печать, максимальное качество |

### В промпте

Всегда добавляйте технические детали качества в раздел "Стиль":
```
8K resolution, ultra high definition, professional quality, highly detailed,
sharp focus corner to corner, crystal clear, intricate fine details visible,
maximum texture resolution
```

---

## Адаптация под контексты

### Фотография портретов
**Акцент:** Текстуры кожи, эмоции, освещение лица, глубина резкости
**Best Practice:** `best-practices/photography-portraits.md`

### Фотография продуктов
**Акцент:** Материалы, студийный свет, чистота фона, точность цветов
**Best Practice:** `best-practices/photography-products.md`

### Инфографика
**Акцент:** Структура информации, типографика, layout logic, точный текст
**Best Practice:** `best-practices/design-infographics.md`

### Презентации
**Акцент:** Negative space для текста, читаемость, title-safe зоны
**Best Practice:** `best-practices/business-presentations.md`

---

## Частые ошибки и решения

### ❌ Ошибка 1: Список тегов вместо сценария

**Плохо:**
```
cat, beach, sunset, golden hour, photorealistic, 4k
```

**Хорошо:**
```
A ginger tabby cat sitting on wet sand at ocean's edge during sunset,
watching waves roll in. Cat's fur catching warm golden light from setting
sun creating rim light effect. Shot with 85mm lens at f/2.8, soft bokeh
background, photorealistic.
```

---

### ❌ Ошибка 2: Отсутствие технических параметров камеры

**Плохо:**
```
Professional portrait of businessman
```

**Хорошо:**
```
Professional portrait of businessman shot on Hasselblad H6D with 80mm f/2.8
lens at f/4, studio lighting with large octagonal softbox, sharp focus on
eyes, 8K resolution
```

---

### ❌ Ошибка 3: Пластиковая кожа в портретах

**Плохо:**
```
Portrait of woman, beautiful skin, professional
```

**Хорошо:**
```
Portrait of woman showing natural skin texture - visible pores, subtle
freckles, vellus hair catching light, subsurface scattering showing warm
undertones, catchlight in eyes, minor imperfections maintaining photorealism
```

---

### ❌ Ошибка 4: Неконкретное описание освещения

**Плохо:**
```
good lighting, professional
```

**Хорошо:**
```
Classic three-point studio lighting - large octagonal softbox as key light
from 45 degrees creating gentle modeling, white reflector fill from opposite
side, subtle rim light from behind for separation, soft even illumination
```

---

### ❌ Ошибка 5: Отсутствие negative prompt

**Плохо:**
```
[Только позитивный промпт без negative]
```

**Хорошо:**
```
[Позитивный промпт]

Negative Prompt: cartoon, illustration, plastic skin, bad quality, deformed
```

---

## Итерация и улучшение

Если результат не удовлетворяет, используйте эту последовательность:

### Шаг 1: Проверьте структуру
- ✅ Все 5 столпов присутствуют?
- ✅ Описание повествовательное, а не теги?
- ✅ Есть negative prompt?

### Шаг 2: Добавьте технические детали
- 📷 Тип камеры (Hasselblad, Canon, Sony)
- 🔍 Фокусное расстояние (35mm, 50mm, 85mm, 100mm, 135mm)
- 🎛️ Диафрагма (f/1.2, f/2.8, f/5.6, f/11)
- 💡 Конкретная схема освещения (Rembrandt, softbox, golden hour)

### Шаг 3: Уточните материалы и текстуры
- Для кожи: pores, freckles, vellus hair, subsurface scattering
- Для тканей: weave pattern, fabric texture, stitching detail
- Для металла: reflections, brushed/polished finish, oxidation
- Для дерева: grain pattern, knots, natural imperfections

### Шаг 4: Увеличьте разрешение
- Если детали размыты → используйте `--image-size 4K`

### Шаг 5: Уточните цветовую палитру
```
Вместо: "warm colors"
Используйте: "warm color palette - golden yellows (#FFD700), burnt oranges
(#CC5500), deep reds (#8B0000), creating cohesive sunset-inspired scheme"
```

---

## Ограничения и безопасность

⚠️ **Запрещенный контент:**
- NSFW / сексуальный контент
- Изображения известных людей без образовательного контекста
- Насилие, gore, травмы
- Вводящий в заблуждение контент (deepfakes)
- Ненависть, дискриминация

✅ **Все изображения содержат SynthID водяной знак** для отслеживания AI-генерации

🔒 **Автоматическая модерация:** Запросы проходят safety filters Google

---

## Полезные ресурсы

**Официальная документация:**
- [Google AI Image Generation Guide](https://ai.google.dev/gemini-api/docs/image-generation)
- [Gemini Gallery](https://gemini.google/gallery/)
- [Google AI Studio](https://aistudio.google.com/)

**Community:**
- [Reddit: r/Bard - Nano Banana Discussion](https://www.reddit.com/r/Bard/)
- [Official Nano Banana Prompting Guide](https://www.reddit.com/r/Bard/comments/1n3wn70/official_nanobanana_prompting_guide_and/)

**Skill Documentation:**
- `SKILL.md` - Основная документация skill
- `best-practices/README.md` - Обзор специализированных гайдов
- `best-practices/*.md` - Детальные гайды по типам контента

---

**Версия:** 2.0
**Дата обновления:** 2026-01-06
**Методология:** "Пять столпов" (Five Pillars) для Reasoning Engine
