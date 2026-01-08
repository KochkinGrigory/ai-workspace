# Best Practices: Мультипликационные Персонажи и Иллюстрация v2.0

> **Версия:** 2.0
> **Назначение:** Руководство для создания стилизованных персонажей, анимации, векторных иллюстраций
> **Модель:** Gemini 3 Pro Image Preview (Nano Banana Pro)
> **Методология:** "От Фотореализма к Стилизации" - адаптация "5 столпов"

---

## Фундаментальная концепция: Стилизация vs Реализм

### 🎨 Парадигма Стилизации

**Ключевое отличие:**

Nano Banana Pro обучена на **всем спектре визуального искусства** - от гиперреализма до абстракции. Понимание того, как модель интерпретирует стилизацию, критично для качественного результата.

**Фотореализм:**
- Физически корректные текстуры (поры кожи, subsurface scattering)
- Реалистичное освещение с точной физикой
- Детальная геометрия лица и тела
- Случайные "несовершенства"

**Стилизация (Мультипликация/Иллюстрация):**
- **Упрощенная геометрия** (меньше полигонов, чистые линии)
- **Преувеличенные пропорции** (большие глаза, маленький нос)
- **Плоские или градиентные цвета** (не фототекстуры)
- **Намеренное совершенство** (симметрия, чистота форм)

---

### От Реализма к Стилизации: Спектр

```
Фотореализм ←→ Арт-реализм ←→ Стилизация ←→ Абстракция
    |              |              |              |
Текстуры      Сглаженные    Упрощенные    Геометрия
Несовер-      текстуры      формы         форм
шенства       Мягкие        Чистые
              контуры       линии
```

**Для управления уровнем стилизации:**
- Больше реализма: "Semi-realistic", "Painterly", "Soft shading"
- Больше стилизации: "Flat colors", "Bold outlines", "Simplified shapes"
- Максимальная стилизация: "Vector art", "Minimalist", "Geometric"

---

## Методология "Пять столпов" для Иллюстрации

Базовая структура сохраняется, но **акценты смещаются** с физической корректности на **визуальную выразительность**.

### 1️⃣ Субъект (Character Design)

**Что описываем:** Визуальный характер персонажа, стилистическую принадлежность.

**Обязательно указать:**
- **Стиль** (аниме, 3D Pixar, векторная иллюстрация, западный мультфильм)
- **Возрастная группа** (chibi, подросток, взрослый)
- **Пропорции тела** (реалистичные, героические, chibi, elongated)
- **Ключевые визуальные элементы** (большие глаза, яркие волосы, уникальная одежда)
- **Цветовая палитра персонажа** (теплая, холодная, пастельная, неоновая)

**Примеры:**

**Аниме персонаж:**
```
Teenage anime girl with large expressive emerald green eyes, long flowing silver
hair with pink highlights. Wearing futuristic school uniform - white blazer with
holographic accents, pleated skirt. Kyoto Animation style character design with
soft shading and detailed hair rendering.
```

**3D Pixar:**
```
Cute 3D character - anthropomorphic orange tabby cat wearing tiny detective coat
and magnifying glass. Pixar-style proportions with oversized head (1:2.5 ratio),
large round eyes with prominent catchlights, soft fur texture with subsurface
scattering. Friendly, approachable design.
```

**Векторная иллюстрация:**
```
Flat vector illustration of young professional woman. Simplified geometric shapes,
Corporate Memphis style. Minimal facial features (dots for eyes, curved line for
smile). Warm color palette - terracotta skin tone, mustard yellow shirt. Clean
linework, no gradients.
```

---

### 2️⃣ Действие (Expression & Pose)

**Что происходит:** В стилизации **эмоции преувеличены**, позы динамичны и выразительны.

**Обязательно указать:**
- **Эмоция** (не просто "happy", а "ecstatic with sparkles in eyes and wide smile")
- **Динамика позы** (action pose, idle pose, hero landing pose)
- **Язык тела** (confident stance, shy posture, aggressive lean)
- **Визуальные эффекты эмоций** (sweat drops, anger marks, heart symbols)

**Примеры:**

**Аниме экшн:**
```
Dynamic action pose - character mid-jump performing spinning kick, legs extended,
one arm sweeping back for balance. Motion blur effects on limbs. Determined facial
expression with focused eyes. Speed lines radiating from center emphasizing
movement energy.
```

**3D персонаж эмоция:**
```
Character in moment of joyful surprise - eyes wide open, mouth in perfect O shape,
hands raised to cheeks. Slight anticipation lean forward. Pixar-style exaggerated
expression with bouncy, energetic body language.
```

**Векторная иллюстрация:**
```
Character sitting at desk working on laptop, relaxed posture. Simple geometric
pose - torso as rounded rectangle, arms as curved lines. Minimal expression -
small smile suggested by single curved line. Static, calm composition.
```

---

### 3️⃣ Окружение (Setting & Atmosphere)

**Где находится:** Стилизованные окружения часто **упрощены** или **концептуальны**.

**Обязательно указать:**
- **Уровень детализации фона** (highly detailed, simple gradient, solid color)
- **Стилистическое соответствие** (фон должен match стилю персонажа)
- **Атмосфера через цвет** (warm afternoon glow, cool night atmosphere, neon cyberpunk)
- **Графические элементы** (sparkles, floating geometric shapes, energy auras)

**Примеры:**

**Аниме background:**
```
Detailed anime-style background - Japanese high school rooftop during sunset.
Makoto Shinkai level detail in sky - dramatic cumulonimbus clouds with orange
and pink gradients. Chain-link fence, water tower silhouette. Lens flare effects
from setting sun. Hyper-detailed environment contrasting with cel-shaded character.
```

**3D сцена:**
```
Isometric 3D room scene - cozy bedroom with toy-like aesthetic. Simplified
furniture - rounded bed, cylindrical lamp, cubic bookshelf. Soft ambient lighting
with subtle ambient occlusion. Pastel color palette - mint green walls, peach
curtains. Octane render quality.
```

**Векторный фон:**
```
Abstract geometric background - overlapping circles and rounded rectangles in
complementary colors (navy blue, coral, cream). Flat design, no shadows or depth.
Clean negative space around character. Modern minimalist aesthetic.
```

---

### 4️⃣ Композиция/Визуальный Язык (Visual Language)

**Как изображено:** В стилизации композиция определяется **визуальным стилем** больше, чем камерой.

**Обязательно указать:**
- **Тип рендеринга** (2D cel shading, 3D render, vector art, watercolor)
- **Контуры** (bold outlines, no outlines, variable line weight)
- **Тени и свет** (cel shading, soft gradient, no shadows, dramatic chiaroscuro)
- **Ракурс** (front view, 3/4 view, profile, isometric, bird's eye)

**Примеры:**

**Аниме визуал:**
```
Front-facing character portrait, slight 3/4 angle turn. Cel shaded rendering with
crisp separation between light and shadow areas. Bold black outlines on character,
thinner lines for internal details. Anime-style highlight streaks in hair. Soft
gradient shading on skin. Digital painting aesthetic.
```

**3D рендер:**
```
Isometric view character render. 3D model rendered in Octane with toon shader.
Rim lighting creating bright edge highlights separating character from background.
Soft ambient occlusion in crevices. Subsurface scattering on skin/fur for soft
glow. Clay-like material aesthetic.
```

**Векторная композиция:**
```
Flat vector art, absolutely no shading or depth. Single-weight clean linework.
Solid color fills - no gradients except for background. Geometric construction
visible (circles for head, rectangles for body). Front-facing symmetrical
composition. Corporate illustration style.
```

---

### 5️⃣ Стиль (Art Style & Aesthetic)

**Визуальная эстетика:** Это **центральный столп** для иллюстрации - определяет весь визуальный язык.

**Обязательно указать:**
- **Художественная школа** (anime, western cartoon, children's book, concept art)
- **Референс студии/художника** (Studio Ghibli, Pixar, Loish, Kurzgesagt)
- **Цветовая обработка** (vibrant saturated, pastel soft, monochromatic, neon)
- **Техника исполнения** (digital painting, vector, 3D render, watercolor)
- **Целевое использование** (game character, marketing mascot, sticker, avatar)

---

## Основные стили: Детальный разбор

### 🇯🇵 СТИЛЬ 1: Аниме и Манга

**Фундаментальные характеристики:**
- Большие выразительные глаза с детальными бликами
- Упрощенные носы (точка или маленький клин)
- Стилизованные рты (линия или простая форма)
- Детальные волосы с отдельными прядями
- Cel shading (четкое разделение света и тени)

#### Ключевые слова и термины:

**Общие:**
- `anime style` - базовый стиль
- `key visual` - высококачественный промо-арт
- `cel shaded` - классическая аниме-заливка
- `bold outlines` - жирные контуры
- `anime eyes` - характерные глаза

**По студиям (Style Reference):**
- `Kyoto Animation style` - детализация, красивые глаза, мягкое освещение
- `Makoto Shinkai style` - гипердетализированные фоны, драматичные облака, lens flares
- `Studio Ghibli style` - акварельная эстетика, теплые тона, nature-focused
- `TRIGGER style` (Kill la Kill, Cyberpunk Edgerunners) - яркие неоновые цвета, динамичные позы
- `Ufotable style` - цифровые эффекты, драматичное освещение

**Технические:**
- `chromatic aberration` - цветовые искажения по краям для динамики
- `sakuga quality` - сверхвысокое качество анимации
- `bishoujo` / `bishounen` - красивая девушка / красивый юноша
- `chibi` - сверхупрощенный милый стиль

#### Пример промпта (Аниме портрет):

```
СУБЪЕКТ:
Anime portrait of mysterious silver-haired female character, late teens. Large
luminous purple eyes with multiple highlight points creating depth. Long flowing
hair with individual strand detail, slight wind movement. Wearing futuristic
tactical outfit - black bodysuit with glowing cyan circuit patterns.

ДЕЙСТВИЕ:
Character making direct eye contact with viewer, slight head tilt showing
confidence. One hand raised touching side of face in thoughtful pose. Calm,
enigmatic expression - small knowing smile.

ОКРУЖЕНИЕ:
Dark background with bokeh light effects - out of focus neon signs creating
colorful circles of light (cyan, magenta, yellow). Subtle particle effects
floating in air suggesting urban rain environment.

КОМПОЗИЦИЯ:
Close-up portrait shot, shoulders and up. Slight 3/4 angle. Cel shaded rendering
with crisp shadow edges. Bold black outlines on character, finer lines on
internal details. Anime-style highlight streaks in hair catching light.

СТИЛЬ:
High-quality anime key visual in Kyoto Animation style. Digital painting aesthetic
with soft gradient shading on skin. Vibrant but not oversaturated color palette.
Professional commercial anime production quality. 4K resolution.

Negative Prompt: photorealistic, 3D render, western cartoon, simple, low quality,
deformed anatomy, multiple heads, bad proportions
```

---

### 🎬 СТИЛЬ 2: 3D Персонажи (Pixar / Game Character)

**Фундаментальные характеристики:**
- Rounded, appealing shapes (squash & stretch принцип)
- Exaggerated proportions (большая голова относительно тела для cuteness)
- Soft materials (subsurface scattering на коже/меху)
- Профессиональное студийное освещение
- High-quality rendering (Octane, Arnold, Cycles)

#### Ключевые слова:

**Базовые:**
- `3D render` - 3D рендер
- `Pixar style` - стиль Пиксар
- `Octane render` / `Arnold render` / `Cycles render` - движки рендеринга
- `subsurface scattering` - подповерхностное рассеивание (мягкость)
- `toon shader` - мультипликационный шейдер

**Пропорции:**
- `chibi proportions` - голова больше тела (1:2 или 1:2.5)
- `heroic proportions` - для супергероев (голова меньше, 1:8)
- `realistic proportions` - близко к реальности (1:7)

**Материалы:**
- `glossy plastic` - глянцевый пластик
- `soft fur texture` - мягкий мех
- `metallic sheen` - металлический блеск
- `matte finish` - матовая поверхность

**Освещение:**
- `three-point lighting` - трехточечное освещение
- `rim lighting` - контровой свет (отделение от фона)
- `ambient occlusion` - затенение в углублениях
- `soft shadows` - мягкие тени

**Контекст:**
- `isometric view` - изометрическая проекция
- `turntable pose` - T-поза для модели
- `character design sheet` - лист разработки персонажа

#### Пример промпта (3D милый персонаж):

```
СУБЪЕКТ:
Adorable 3D character - anthropomorphic red panda wearing tiny explorer outfit.
Chibi proportions (head to body ratio 1:2.5). Oversized round head with huge
sparkling brown eyes and prominent catchlights. Soft fluffy fur texture with
orange-red and cream colors. Wearing miniature khaki vest with tiny pockets,
small backpack. Round paws, stubby tail.

ДЕЙСТВИЕ:
Character in excited discovery pose - standing on hind legs, one paw raised
pointing upward with index finger, mouth open in joyful expression showing tiny
teeth. Eyes wide with wonder. Body language conveying "Eureka!" moment.

ОКРУЖЕНИЕ:
Simple clean studio environment - soft gradient background transitioning from
warm cream to light blue. Floating geometric shapes (circles, triangles) in
pastel colors creating playful atmosphere. Soft diffused lighting, no harsh
elements.

КОМПОЗИЦИЯ:
3/4 view slightly from below (low angle) making character feel heroic despite
small size. Rendered in Octane with toon shader combining 3D depth with
cartoon aesthetic. Three-point lighting - key light from upper left (warm),
fill light from right (cool), rim light from behind separating from background.
Subtle ambient occlusion around paws and under tail.

СТИЛЬ:
Pixar-quality 3D character render. Subsurface scattering on fur creating soft
glow when backlit. Glossy eyes with complex multi-layer reflections. Soft
shadows with gradient falloff. Toy-like aesthetic suitable for blind box
collectible or game mascot. Vibrant but harmonious color palette. 4K resolution
with high detail level.

Negative Prompt: realistic, photographic, 2D flat, anime style, dark atmosphere,
complex background, messy, scary, aggressive
```

---

### 📐 СТИЛЬ 3: Векторная Иллюстрация (Flat Design)

**Фундаментальные характеристики:**
- Абсолютно плоские цвета (no gradients или минимальные)
- Геометрическая конструкция форм
- Чистые линии или их отсутствие
- Минималистичные детали лица
- Используется в UI/UX, инфографике, брендинге

#### Ключевые слова:

**Стиль:**
- `flat vector art` - плоская векторная графика
- `flat design` - плоский дизайн
- `geometric illustration` - геометрическая иллюстрация
- `minimalist illustration` - минималистичная иллюстрация
- `Corporate Memphis` - популярный корпоративный стиль (Facebook, Airbnb)

**Технические:**
- `clean lines` - чистые линии
- `no gradients` - без градиентов
- `solid colors` - сплошные цвета
- `simple shapes` - простые формы
- `no shadows` - без теней (или `long shadow` - длинная тень)

**Композиция:**
- `centered composition` - центрированная
- `negative space` - негативное пространство
- `balanced layout` - сбалансированная компоновка

#### Пример промпта (Векторная иллюстрация):

```
СУБЪЕКТ:
Flat vector illustration of young female designer working. Character constructed
from simple geometric shapes - circle for head, rounded rectangle for torso,
cylinders for limbs. Minimal facial features - two dots for eyes, small curved
line for smiling mouth, simple curved line suggesting nose. Hair represented as
solid shape with no individual strands - bob cut in deep teal color. Wearing
burnt orange sweater (solid color block), navy blue pants.

ДЕЙСТВИЕ:
Character sitting at desk in relaxed working pose. Arms positioned at laptop
(suggested by simple rectangle shape). Body slightly leaned forward showing
engagement. Pose constructed from basic geometric primitives - curved lines for
arms, angled rectangles for legs. Static, calm composition.

ОКРУЖЕНИЕ:
Minimal workspace environment - desk as simple horizontal plane (warm wood tone),
laptop as flat rectangle, potted plant as circle (leaves) on cylinder (pot) in
sage green. Background - solid warm cream color with optional decorative geometric
elements (abstract circles and lines in muted coral and mustard yellow) floating
in composition corners. Clean negative space around central subject.

КОМПОЗИЦИЯ:
Flat 2D composition, no perspective or depth. All elements on same visual plane.
Absolutely no shading, shadows, or gradients on character. Background may have
subtle gradient (cream to light peach) but character strictly flat colors.
Symmetric and balanced layout. Objects constructed from overlapping shapes with
clean edges.

СТИЛЬ:
Corporate Memphis / Alegria illustration style. Modern, friendly, approachable
aesthetic. Warm color palette - terracotta, mustard yellow, teal, navy, cream.
Clean vector artwork suitable for web UI, marketing materials, or presentations.
Professional but playful tone. Inspirations: Airbnb, Headspace, Dropbox
illustration systems.

Negative Prompt: realistic, 3D, shadows, textures, gradients (on character),
detailed, photographic, anime, complex, cluttered
```

---

### 🎨 СТИЛЬ 4: Western Cartoon / Cartoon Network Style

**Фундаментальные характеристики:**
- Более угловатые формы по сравнению с аниме
- Вариативная толщина линий (line weight variation)
- Преувеличенные позы и экспрессии
- Часто более "грубый", энергичный стиль

#### Ключевые слова:

- `western cartoon style` - западный мультипликационный стиль
- `Cartoon Network style` - стиль мультов CN
- `thick outlines` - толстые контуры
- `exaggerated features` - преувеличенные черты
- `dynamic pose` - динамичная поза
- `squash and stretch` - сплющивание и растяжение (анимационный принцип)
- `expressive` - выразительный

**Референсы стилей:**
- `Steven Universe style` - мягкие округлые формы, пастель
- `Adventure Time style` - простые формы, noodle limbs
- `Gravity Falls style` - детализированные фоны, character variety
- `Rick and Morty style` - более детальный, sci-fi элементы

#### Пример промпта (Western Cartoon):

```
СУБЪЕКТ:
Western cartoon-style superhero character. Exaggerated heroic proportions - broad
square shoulders, muscular arms with simplified anatomy, narrow waist. Angular
face with strong square jaw, determined expression. Costume - bright red cape,
blue bodysuit with yellow lightning bolt emblem. Bold black outlines with variable
line weight (thicker on outer edges, thinner for details).

ДЕЙСТВИЕ:
Dynamic action pose - character in mid-flight, one fist extended forward, cape
billowing behind creating dramatic diagonal. Squash and stretch principle applied
to body showing motion and impact. Determined facial expression with narrowed
eyes, clenched jaw.

ОКРУЖЕНИЕ:
Simplified cityscape background with angular buildings. Cartoon-style clouds as
simple rounded shapes. Motion lines and speed effects around character. Bright
primary color palette - blues, reds, yellows. High contrast between character
and background.

КОМПОЗИЦИЯ:
Dynamic angle shot from below making character appear heroic and powerful. Thick
black outlines on all elements. Cel shaded with flat colors and minimal gradient.
Simple shadow shapes in darker tones.

СТИЛЬ:
Classic Western superhero cartoon in style of DC Animated Universe. Bold, clean
graphic style. Saturated primary colors. Energy and movement emphasized through
angular shapes and dynamic composition. Commercial animation quality.

Negative Prompt: anime, realistic, 3D render, soft, pastel, minimalist, complex
shading, photographic
```

---

## 🔄 Консистентность Персонажей в Сериях

**КРИТИЧНО:** При создании серий изображений одного персонажа в разных позах/ракурсах.

### Стратегия "Character Foundation" (Базовый Персонаж)

#### Шаг 1: Создание эталонного изображения

**Генерация Character Sheet (Model Sheet):**

```
Character design sheet for [описание персонажа]. Show three views on single
image: front view (facing camera), side profile view (90 degrees), and back view.
T-pose with arms slightly spread. Clean, neutral expression. White background,
even studio lighting with no dramatic shadows. [Style specifications]. This is
a model sheet for animation reference.
```

**Пример для аниме персонажа:**
```
Character design sheet for teenage anime girl with short blue hair and yellow
eyes. Front view, side profile, and back view on single canvas. Wearing school
uniform - white shirt, red ribbon tie, pleated navy skirt. T-pose stance. Clean
linework, cel shaded. Kyoto Animation style. White background, neutral lighting.
Character turnaround for animation reference.
```

**Результат:** Получите изображение с тремя ракурсами персонажа на одном холсте.

---

#### Шаг 2: Разделение и использование как референса

После генерации:
1. Crop изображение на 3 части (фронт, профиль, спина)
2. Используйте эти изображения как reference images для последующих генераций

---

#### Шаг 3: Генерация серии с консистентностью

**Для каждой последующей генерации:**

```
Same character from reference images [attach model sheet views]. Now [новое
действие/поза/окружение]. CRITICAL: Maintain 100% facial consistency, hair
style, clothing, and body proportions from reference. Only change pose and
environment. [Style должен совпадать с референсом].
```

**Пример серии (3 изображения):**

**Изображение 1 (эталон):**
```
Anime character turnaround sheet - cute girl with twin-tail pink hair, green
eyes, wearing magical girl outfit (white dress with pink ribbons). Front, side,
back views. T-pose. Clean cell shading, white background.
```

**Изображение 2 (с референсом на 1):**
```
Same character from reference image. Now in dynamic magical girl transformation
pose - spinning with arms raised, ribbons flowing around. Sparkle and star
effects. Maintain exact facial features, hair style, and outfit from reference.
Magical background with pink and white light rays. Kyoto Animation style.
```

**Изображение 3 (с референсом на 1):**
```
Same character from reference. Sitting on park bench eating ice cream, relaxed
casual pose, gentle smile. Maintain identical appearance from reference - same
pink twin-tails, green eyes, white magical dress. Outdoor park setting with
trees, afternoon sunlight. Same cel shading style.
```

---

### Identity Lock Syntax (Синтаксис фиксации идентичности)

**Критические фразы для промптов 2+:**

```
- "Same character from reference image(s)"
- "Maintain 100% facial consistency with reference"
- "Keep exact same [hair style / outfit / proportions] as reference"
- "Preserve character identity from reference"
- "Do not alter facial features from reference"
- "Only change [pose / action / environment], keep character identical"
```

---

### Troubleshooting консистентности

| Проблема | Причина | Решение |
|----------|---------|---------|
| Лицо изменилось | Слабая привязка к референсу | Добавить "Maintain 100% facial features from reference" |
| Изменился цвет волос/одежды | Модель интерпретировала текст | Загрузить ЦВЕТНОЙ эталон, указать "Use exact colors from reference" |
| Пропорции отличаются | Конфликт между текстом и изображением | Убрать из промпта описание пропорций, оставить только "from reference" |
| Стиль рендеринга изменился | Не указан стиль повторно | Всегда повторять style keywords из эталона |

---

## Negative Prompts по стилям

### Для Аниме:
```
photorealistic, 3D render, western cartoon, realistic proportions, detailed skin
texture, pores, ugly, deformed, bad anatomy, extra limbs, poorly drawn hands,
poorly drawn face, mutation, low quality, blurry
```

### Для 3D Pixar:
```
2D, flat, anime, realistic human, photographic, dark, scary, complex background,
low poly, unrendered, sketch, wireframe, bad topology, deformed, low quality
```

### Для Векторной графики:
```
3D, realistic, photographic, shadows, gradients (on character), textures,
detailed, complex, messy, anime, sketch, painterly, blurry
```

### Для Western Cartoon:
```
anime, realistic, 3D render, photographic, soft, detailed shading, complex
rendering, muted colors, minimalist, low energy
```

---

## Продвинутые техники

### Техника 1: Style Blending (Смешивание стилей)

Можно комбинировать элементы разных стилей:

```
Character design combining anime facial features (large expressive eyes) with
western cartoon body proportions (exaggerated muscular build). Pixar-quality 3D
rendering with anime-style hair shading. Hybrid aesthetic.
```

### Техника 2: Collab Art (Коллаборация с фото)

Загрузите своё селфи и попросите:

```
Transform person in photo into [anime character / Pixar character / cartoon].
Maintain facial structure and proportions but apply [style] aesthetic. Keep
person recognizable but fully stylized.
```

### Техника 3: Sticker/Emoji Design

```
Cute chibi sticker design of [character]. Super deformed proportions (head 70%
of total height). Simplified features, minimal detail. Thick black outline.
Transparent background. Designed for messaging app stickers.
```

---

## Полные примеры промптов

### Пример 1: Игровой Персонаж (Character Concept Art)

```
1. СУБЪЕКТ:
Fantasy RPG character concept art - elven archer ranger. Slender athletic build,
pointed ears, long braided platinum blonde hair with leaf ornaments. Wearing
leather armor with forest-green cloak, quiver of arrows on back, ornate bow in
hand. Semi-realistic anime-inspired style with detailed costume design.

2. ДЕЙСТВИЕ:
Standing in confident ready pose, bow held diagonally across body, one hand on
bowstring. Alert expression scanning horizon. Weight shifted onto back leg,
front foot forward - ready to move stance.

3. ОКРУЖЕНИЕ:
Simple gradient background - forest green fading to misty white. Minimal
environmental elements - few floating leaves, subtle magic particle effects
around character suggesting nature affinity.

4. КОМПОЗИЦИЯ:
Full body character shot, slight 3/4 angle view. Digital painting style with
soft cel shading creating volume without photorealistic texture. Clean linework
defining costume details and anatomy. Soft gradient shadows.

5. СТИЛЬ:
Professional game character concept art in style of Genshin Impact / Honkai
Star Rail. Anime-influenced but with more realistic proportions and detailed
costume design. Rich colors - forest greens, browns, gold accents. High detail
on costume and equipment, softer rendering on skin and hair. Suitable for game
character presentation or art book. 4K resolution.

Negative Prompt: photorealistic, pure anime, chibi, western cartoon, 3D render,
simple, low detail, bad anatomy, deformed
```

---

### Пример 2: Маскот для Бренда (Brand Mascot)

```
1. СУБЪЕКТ:
Friendly 3D brand mascot character - anthropomorphic light bulb with arms and
legs. Bulb body made of glossy glass (transparent with warm yellow inner glow),
metal screw base as feet, simple cartoon arms with white gloves. Large friendly
eyes with prominent shine, wide smile showing enthusiasm. Cute chibi proportions.

2. ДЕЙСТВИЕ:
Character in welcoming gesture - both arms spread wide, slight forward lean
showing eagerness to help. One leg slightly raised in dynamic friendly pose.
Excited happy expression radiating positive energy.

3. ОКРУЖЕНИЕ:
Clean studio setting with soft gradient background - light blue to white creating
professional yet friendly atmosphere. Subtle floating sparkle effects around
character suggesting innovation and bright ideas.

4. КОМПОЗИЦИЯ:
Isometric 3/4 view making character equally visible from multiple angles. Rendered
in Octane with toon shader for cartoon aesthetic with 3D depth. Three-point
lighting - soft key light from front-left, subtle rim light from behind creating
glow effect on glass bulb, gentle fill light preventing harsh shadows.

5. СТИЛЬ:
Pixar-quality 3D character render optimized for brand mascot use. Subsurface
scattering on glass bulb creating realistic inner glow. Glossy reflective
materials. Soft friendly aesthetic suitable for tech company or educational
platform. Vibrant but professional color palette. Design works at any scale
from app icon to billboard. 4K resolution.

Negative Prompt: realistic, dark, complex, scary, aggressive, 2D flat, low
quality, messy
```

---

### Пример 3: Иллюстрация для Соцсетей (Social Media Illustration)

```
1. СУБЪЕКТ:
Flat vector illustration of diverse group of three young professionals
collaborating. Characters constructed from simple geometric shapes. Person 1:
woman with afro hair (circle shape) in yellow shirt. Person 2: man with short
hair in coral sweater. Person 3: woman with ponytail in teal top. Minimal
facial features - dots for eyes, curved lines for smiles. Warm skin tones in
different shades showing diversity.

2. ДЕЙСТВИЕ:
Three characters gathered around laptop (simple rectangle) in collaborative
discussion. Gestures suggesting teamwork - one pointing at screen, one with
hand raised in idea gesture, one taking notes. Static poses constructed from
basic geometric forms.

3. ОКРУЖЕНИЕ:
Minimal workspace with essential elements only - desk as horizontal plane,
laptop, coffee cups (cylinders with handles), notebook (rectangle). Background
- solid warm cream color with decorative abstract shapes (circles, rounded
rectangles) in muted complementary colors (sage green, dusty rose, mustard)
floating in corners. Clean negative space.

4. КОМПОЗИЦИЯ:
Flat 2D composition, no perspective. All elements on same plane. Absolutely no
shadows or gradients on characters. Simple overlapping shapes creating depth
through layering only. Balanced symmetrical layout.

5. СТИЛЬ:
Corporate Memphis / Alegria style. Modern friendly illustration for LinkedIn
post or business blog. Warm inclusive color palette promoting diversity and
collaboration. Clean vector aesthetic suitable for web and social media. Style
matching Slack, Asana, Monday.com illustration systems. Professional but
approachable and optimistic tone.

Negative Prompt: realistic, 3D, photographic, shadows on characters, gradients,
complex details, anime, dark, serious, cluttered
```

---

## Заключение

Создание quality стилизованных персонажей и иллюстраций с Nano Banana Pro требует:

**Ключевые правила успеха:**

1. **Явно указывай стиль** - не надейся, что модель угадает
2. **Используй референсы студий/художников** - "Pixar style", "Kyoto Animation"
3. **Для консистентности - создавай Character Sheet** первым изображением
4. **Понимай материальность стиля** - плоские цвета vs 3D рендер vs cel shading
5. **Адаптируй "5 столпов"** - акцент на стиль и выразительность, а не физику
6. **Negative prompts критичны** - предотвращают смешивание несовместимых стилей

**Для каждого стиля используй:**
- Аниме → cel shading, bold outlines, studio references
- 3D → render engine, lighting setup, material properties
- Векторная → geometric construction, flat colors, minimal details
- Western Cartoon → exaggerated proportions, dynamic poses, thick lines

Соблюдение этих принципов позволит создавать консистентных персонажей профессионального качества для любых целей - от игровых концептов до брендовых маскотов.

---

**Версия:** 2.0
**Дата:** 2026-01-06
**Методология:** "От Фотореализма к Стилизации" + "5 столпов" адаптация
