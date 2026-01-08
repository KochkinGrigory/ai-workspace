# Best Practice: Предметная фотосъемка (Product Photography)

Профессиональное руководство по созданию студийных и рекламных изображений товаров с использованием методологии "Виртуальная Студия" для Nano Banana Pro.

## Когда использовать

- Товары для интернет-магазинов (e-commerce)
- Каталоги продукции и меню
- Рекламные материалы и баннеры
- Упаковка и этикетки
- Lifestyle контент для соцсетей
- Презентация новых продуктов

---

## Фундаментальная концепция: Виртуальная Студия

### От тегов к режиссуре съемки

Nano Banana Pro (Gemini 3 Pro Image Preview) использует архитектуру **Reasoning Engine** (Движок Рассуждений), которая фундаментально отличается от старых диффузионных моделей. Модель не "рисует по ключевым словам", а **симулирует реальную фотосессию**.

**Критическое различие:**

❌ **Старый подход (теги):**
```
product, white background, professional, 4k, studio lighting
```

✅ **Новый подход (виртуальная студия):**
```
Commercial product photography of premium headphones shot in professional studio.
Camera: Hasselblad medium format with 100mm macro lens at f/8 for full sharpness.
Lighting setup: Three-point studio lighting - large octagonal softbox as key light
from 45 degrees creating soft shadows, white reflector opposite for fill,
subtle rim light from behind to separate product from background.
Product placement: Headphones positioned at 3/4 angle on infinity white seamless
background, all details in perfect focus from ear cups to headband stitching.
Details: Visible material textures - brushed aluminum finish on ear cups,
genuine leather padding grain, matte black coating on headband.
Style: Clean e-commerce photography with accurate color representation, 4K resolution.
```

### Почему это работает

Модель **планирует сцену** перед рендерингом:
1. Анализирует физические свойства материалов (как свет отражается от металла vs кожи)
2. Просчитывает геометрию теней от источников света
3. Понимает глубину резкости от указанной диафрагмы (f/8, f/2.8)
4. Воссоздает реалистичные блики и отражения

Это означает, что вы работаете не с "генератором картинок", а с **виртуальным фотографом**, которому нужно дать техническое задание.

---

## Пять Столпов для Предметной Съемки

Анатомия идеального промпта для продуктовой фотографии базируется на той же архитектуре "5 столпов", но с адаптацией под специфику предметной съемки.

### 1. Субъект (Subject) - Детальное описание продукта

**Что указывать:**
- Точное название продукта
- Материалы: металл (brushed aluminum, polished chrome), пластик (matte, glossy), стекло, кожа, ткань
- Цвет с оттенками: не просто "синий", а "navy blue" или "midnight blue"
- Финиш/покрытие: glossy (глянцевый), matte (матовый), satin (сатиновый), metallic (металлик)
- Размер/пропорции (если важно для композиции)
- Состояние: новый, с капельками воды, замороженный, с паром и т.д.

**Примеры:**
- ❌ Слабо: "Часы"
- ✅ Хорошо: "Luxury chronograph wristwatch, brushed stainless steel case, black crocodile leather strap, sapphire crystal face"
- ❌ Слабо: "Бутылка вина"
- ✅ Хорошо: "Premium red wine bottle, dark emerald glass with embossed gold foil label, cork sealed with wax stamp"

### 2. Действие (Action) - Взаимодействие с окружением

Даже статичные продукты имеют "действие" через физические эффекты:

**Динамические эффекты:**
- Конденсат на холодных напитках: "condensation droplets forming on bottle surface"
- Пар от горячих продуктов: "gentle steam rising from coffee cup"
- Брызги жидкости: "water splash frozen mid-air around bottle"
- Плавающие элементы: "ice cubes suspended in air around glass"
- Световые блики: "light rays creating star-shaped reflections on faceted crystal"

**Статическая презентация:**
- "Standing upright on pedestal"
- "Laying flat in organized arrangement"
- "Tilted at 15-degree angle for dynamic composition"
- "Partially unwrapped showing product inside packaging"

### 3. Окружение (Location/Context) - Студийная среда или lifestyle сцена

**Три главных типа окружения:**

**A) Infinity Background (для e-commerce):**
```
Pure white infinity seamless background (cyc wall),
no visible horizon line, perfectly even tone, product floating in space
```

**B) Surface + Background (студийная композиция):**
```
Product placed on white marble surface with subtle gray veins,
soft gray gradient background, clean minimal setting
```

**C) Lifestyle Context (в использовании):**
```
Modern kitchen countertop, natural oak wood texture,
coffee brewing accessories arranged around main product,
soft morning sunlight from window, lived-in atmosphere
```

### 4. Композиция (Composition/Camera) - Виртуальная операторская работа

**Focal Length для продуктов:**

| Объектив | Фокусное расстояние | Эффект | Применение |
|----------|---------------------|--------|------------|
| Standard | 50mm | Нейтральная перспектива | Общие планы продуктов |
| Portrait | 85mm | Легкая компрессия пространства | Бутылки, упаковки |
| Macro | 100mm Macro | Экстремная детализация | Ювелирка, текстуры, еда |
| Wide | 35mm | Показ окружения | Lifestyle сцены |

**Aperture (Диафрагма) для продуктов:**

- **f/8 - f/11:** Полная резкость (весь продукт в фокусе) - стандарт для каталогов
- **f/4 - f/5.6:** Умеренное размытие фона - для акцента на главном элементе
- **f/2.8 - f/4:** Мягкое боке - для lifestyle и рекламных съемок

**Углы съемки:**

```
# E-commerce стандарт
3/4 view (three-quarter angle), slightly elevated camera position,
showing front and side of product for dimensional representation

# Flat Lay
Bird's eye view, shot from directly above, all elements arranged symmetrically

# Hero Shot
Low angle shot looking slightly upward, dramatic perspective emphasizing premium quality

# Detail Shot
Extreme close-up macro focusing on craftsmanship, texture, logo detail
```

### 5. Стиль (Style) - Эстетика и назначение

**E-commerce / Catalog:**
```
Clean professional product photography, accurate color representation,
no artistic effects, commercial catalog style, high detail
```

**Advertising / Hero:**
```
High-end commercial advertising photography, dramatic lighting,
premium luxury aesthetic, cinematic quality, magazine-worthy
```

**Lifestyle / Editorial:**
```
Natural lifestyle photography, organic composition, relatable setting,
Instagram-worthy aesthetic, authentic and approachable
```

---

## Освещение для Продуктов: Студийные схемы

### Схема 1: Even Studio Lighting (Равномерное студийное освещение)

**Применение:** E-commerce, каталоги, технические товары

**Описание:**
```
Studio lighting setup with two large softboxes positioned at 45-degree angles
on both sides, creating perfectly even illumination with no harsh shadows.
White reflector beneath product for fill light, eliminating any underside shadows.
Result: Bright, clean, shadow-free presentation showing all product details clearly.
```

**Характеристики:**
- Нет жестких теней
- Все детали видны
- Точная передача цвета
- Профессиональный каталожный вид

### Схема 2: Rim Lighting (Контровой свет)

**Применение:** Стеклянные изделия, бутылки, прозрачные продукты

**Описание:**
```
Backlit product photography with strong rim light positioned behind and above product,
creating bright glowing edges that separate product from background.
Key light from front at reduced power to show product details without overpowering rim effect.
Result: Dramatic edge glow, visible transparency, premium presentation.
```

**Характеристики:**
- Светящийся контур
- Отделение от фона
- Подчеркивание формы
- Эффектная драматургия

### Схема 3: Soft Window Light (Мягкий оконный свет)

**Применение:** Lifestyle, натуральная косметика, органические продукты

**Описание:**
```
Natural soft diffused light from large north-facing window,
positioned at 45-degree angle to product creating gentle directional shadows.
White bounce card on opposite side to open up shadows.
Warm morning light quality, authentic and inviting atmosphere.
```

**Характеристики:**
- Естественный вид
- Мягкие тени
- Теплые тона
- Атмосферная подача

### Схема 4: Dramatic Side Lighting (Драматический боковой свет)

**Применение:** Премиальные товары, алкоголь, парфюмерия

**Описание:**
```
Single powerful light source positioned at hard 90-degree side angle,
creating strong contrast with deep shadows on opposite side.
Subtle fill reflector to retain some detail in shadows without losing drama.
Dark gradient background, moody and luxurious atmosphere.
```

**Характеристики:**
- Высокий контраст
- Глубокие тени
- Роскошный вид
- Художественная подача

---

## Материалы и Текстуры: Фотореализм через детали

Для фотореалистичных продуктов критически важно описывать **физические свойства материалов**. Nano Banana Pro понимает, как разные материалы взаимодействуют со светом.

### Металлы

**Ключевые слова:**
```
Brushed aluminum (матовый алюминий) - linear grain texture, soft reflections
Polished chrome (хром) - mirror-like reflections, sharp highlights
Brushed stainless steel - directional grain, subtle reflections
Matte black metal - no reflections, powder-coated finish
Rose gold - warm metallic tone, luxury finish
Gunmetal gray - dark metallic with subtle sheen
```

**Пример промпта:**
```
Close-up product photography of luxury pen, brushed titanium body with
visible linear grain texture running lengthwise, subtle directional reflections
from studio lights creating highlight strips along edges, rose gold clip
with polished finish showing sharp light reflections, matte black grip section
with no reflections, macro lens showing all surface details.
```

### Стекло и прозрачные материалы

**Ключевые слова:**
```
Crystal clear glass - perfect transparency, sharp refraction
Frosted glass - translucent, diffused light passing through
Colored glass - tinted transparency with light transmission
Condensation droplets - water beads on cold surface
Reflections and refractions - light bending through glass
```

**Пример промпта:**
```
Product photography of premium vodka bottle, crystal clear glass showing
liquid inside with perfect transparency, condensation droplets forming
realistic water beads on surface, light refracting through bottle creating
rainbow edge effects, embossed glass logo visible through transparency,
backlit setup showing glass thickness and clarity.
```

### Ткани и мягкие материалы

**Ключевые слова:**
```
Woven fabric texture - visible thread pattern
Leather grain - natural pebbled texture, subtle creases
Velvet - soft nap surface, directional sheen
Cotton - matte finish, soft draping
Silk - high sheen, flowing fabric
Cashmere knit - visible stitch pattern, soft texture
```

**Пример промпта:**
```
Product flat lay photography of cashmere sweater, soft beige color
with clearly visible fine knit stitch pattern, natural fabric texture
showing individual yarn strands, gentle fabric folds creating soft shadows,
matte finish with subtle natural sheen in highlights, top-down view
with entire sweater in sharp focus showing craftsmanship.
```

### Пищевые продукты

**Ключевые слова для реализма:**
```
Glistening moisture - visible juice, oil droplets
Steam wisps - hot food with rising vapor
Melting effect - ice cream, cheese, chocolate
Crispy texture - visible golden-brown crust
Fresh cut - exposed interior showing layers
Condensation - cold beverages with water drops
```

---

## Детальные Примеры по Категориям

### Пример 1: E-commerce Электроника (Чистый каталог)

**Тип:** Смартфон для интернет-магазина

```
Professional e-commerce product photography of flagship smartphone.
Subject: Latest model smartphone with edge-to-edge OLED display showing
default lock screen, aerospace-grade aluminum frame in midnight blue finish
with matte coating, triple camera array with sapphire crystal lenses visible
on back, device positioned at precise 3/4 angle showing screen and side profile.
Environment: Positioned on pure white infinity seamless background (cyc wall)
with no visible horizon line, product appears to float in perfectly white space.
Lighting: Professional three-point studio lighting setup using large octagonal
softboxes at 45-degree angles on both sides creating perfectly even illumination,
white reflector card beneath device to eliminate any underside shadows, subtle
overhead light creating small catchlights on screen surface showing glass quality.
Camera: Shot on medium format Hasselblad camera with 100mm macro lens, aperture
set to f/11 ensuring entire device from front edge to back edge in razor-sharp focus,
no depth of field falloff, every detail crystal clear.
Details: Visible brushed aluminum texture on frame edges, individual camera lens
elements, screen reflection showing studio lights, power button and volume controls
clearly defined, USB-C port visible.
Style: Clean commercial catalog photography, accurate color representation for
online shopping, no artistic effects, professional quality suitable for product
listing, 4K resolution with perfect edge sharpness.

Negative Prompt: Shadows, gradient background, blur, artistic effects, fingerprints,
smudges, lens flare, oversaturation.
```

### Пример 2: Lifestyle Food Photography (Атмосферная подача)

**Тип:** Латте для кафе/Instagram

```
Lifestyle food photography of artisan cappuccino in ceramic cup.
Subject: Hand-crafted cappuccino in rustic beige ceramic cup with visible pottery
texture and natural glaze imperfections, perfectly executed latte art showing
delicate rosetta leaf pattern in microfoam, rich caramel-brown crema with
tiny bubbles visible, coffee cup sitting on matching saucer.
Action: Gentle wisps of steam rising from hot coffee surface creating atmospheric
effect, barista's hand (cropped at wrist) just releasing cup after placement,
slight motion blur on steam emphasizing freshness and warmth.
Environment: Positioned on natural oak wood cafe table with visible wood grain
and character marks, white ceramic plate with almond croissant (partially eaten)
in background blurred at f/2.8, green potted succulent plant soft focus in far
background, morning cafe setting.
Lighting: Soft natural window light from left side at 45-degree angle creating
gentle directional shadows on right side of cup, warm morning light quality
with color temperature around 4500K, bounce reflector on right maintaining
detail in shadow areas without eliminating depth, overall warm and inviting mood.
Camera: Shot on 50mm prime lens at f/2.8 aperture creating shallow depth of field,
cappuccino cup in perfect sharp focus showing latte art detail and coffee texture,
background elements softly blurred with creamy bokeh, camera positioned at slight
downward angle showing top of coffee and context, natural eye-level perspective.
Details: Visible coffee crema microbubbles, ceramic glaze texture with light
reflections, steam particles catching light, wood grain patterns, condensation
beginning to form on cold water glass in background.
Style: Authentic lifestyle coffee photography, Instagram-worthy aesthetic, warm
color grading with emphasis on browns and creams, natural and organic feel,
editorial magazine quality, cozy morning vibe.

Negative Prompt: Artificial studio lighting, cold tones, oversaturated colors,
fake steam, plastic cup, generic stock photo look.
```

### Пример 3: Premium Advertising (Роскошная презентация)

**Тип:** Парфюм для рекламной кампании

```
High-end commercial advertising photography of luxury perfume bottle.
Subject: Designer perfume in architectural glass bottle, faceted rectangular
design with heavy crystal-clear glass, embossed brand logo on front face,
18-karat gold-plated cap with knurled texture, pale pink fragrance liquid
visible through transparent glass, bottle dimensions emphasizing premium weight
and substantial presence.
Action: Product hero shot with dynamic elements - fresh pink peony petals
suspended in air around bottle as if caught mid-fall, single water droplet
frozen on bottle shoulder catching light, gold confetti particles floating
in background suggesting luxury and celebration.
Environment: Bottle standing on polished black marble pedestal with white
veining creating elegant base, dark charcoal gray gradient background
transitioning from deep black at edges to lighter gray behind product,
minimalist high-end presentation focusing all attention on perfume.
Lighting: Dramatic side lighting from hard light source at 75-degree angle
creating strong contrast, bright highlight strip running down glass bottle
edge showing faceted design, rim light from behind creating luminous glow
around bottle silhouette and gold cap, controlled reflections in marble
surface below, spotlight effect with product brightly lit against darker
background.
Camera: Shot on 85mm portrait lens at f/4 aperture, perfume bottle in
razor-sharp focus from base to cap showing every facet and embossed detail,
floating petals with slight motion blur suggesting movement, background
smoothly graduated, low angle shot (15 degrees below eye level) giving
bottle monumental premium presence.
Details: Visible glass facets with light refraction creating prismatic effects,
embossed logo with dimensional depth and shadow, gold cap with visible knurled
texture pattern catching highlights, liquid perfume color showing clarity,
reflections in polished marble showing bottle underside, individual petal
veins and natural texture, water droplet with realistic surface tension
and internal refraction.
Style: Ultra-premium advertising photography, Vogue/Harper's Bazaar editorial
aesthetic, dramatic lighting creating mood and luxury, cinematic quality,
expensive perfume commercial visual language, museum-quality presentation,
suitable for luxury magazine full-page ad, 4K resolution.

Negative Prompt: Cheap looking, flat lighting, white background, simple
presentation, artificial flowers, fake water, digital-looking effects,
over-processed, cartoon style.
```

### Пример 4: Product Family (Линейка продуктов)

**Тип:** Набор косметики для каталога

```
Professional product family photography of skincare collection.
Subject: Complete 5-piece luxury skincare set arranged in organized layout -
cleanser pump bottle (120ml), toner spray (100ml), serum dropper bottle (30ml),
day cream jar (50ml), night cream jar (50ml). All bottles in consistent
design language: frosted white glass containers with rose gold aluminum caps,
minimalist sans-serif typography, each product clearly labeled.
Arrangement: Products arranged in ascending height order from left to right
creating pleasing visual flow, main product (serum) positioned in center
as hero item slightly forward, supporting products flanking on both sides,
all items aligned on invisible baseline, spacing between items proportional
and balanced.
Environment: Positioned on white Carrara marble surface with subtle gray
veining providing luxury texture, pure white seamless background rising
behind products, clean minimal presentation, marble surface reflecting
products creating subtle mirrored effect beneath.
Lighting: Even studio lighting setup with large octagonal softbox as key
light from front creating soft shadows falling behind and to right of
products, white reflector fill from left side opening up shadows on frosted
glass, overhead softbox providing separation light preventing products
from blending with background, bright and clean commercial lighting showing
all details clearly.
Camera: Shot on 100mm macro lens at f/8 aperture ensuring entire product
family in perfect sharp focus from front bottles to back, straight-on
eye-level camera position showing products as customers would view them
on shelf, no dramatic angles, honest catalog representation.
Details: Visible frosted glass texture with finger-resistant coating, rose
gold cap with brushed metal finish, product labels with crisp typography,
liquid levels visible through translucent bottles, subtle reflections in
marble surface, dust-free pristine presentation, embossed brand logo on
caps catching light.
Style: Clean professional catalog photography, accurate color representation
essential for e-commerce, no artistic effects or excessive retouching,
trustworthy product presentation, pharmaceutical-grade quality standards,
suitable for brand website hero image, 4K resolution with perfect sharpness
across entire frame.

Negative Prompt: Messy arrangement, inconsistent lighting across products,
some items blurred, dramatic shadows, colored background, artistic blur,
products touching each other, cluttered composition.
```

---

## Негативные промпты для устранения артефактов

Используйте negative prompts для предотвращения типичных проблем продуктовой фотографии:

**Универсальный негативный промпт для продуктов:**
```
Low quality, blurry, out of focus, dirty background, harsh shadows,
overexposed, underexposed, unrealistic colors, artificial looking,
3D render look, plastic appearance, bad lighting, cluttered, messy,
watermark, text overlay, distorted proportions, bad perspective,
amateur photography
```

**Для еды:**
```
Unappetizing, artificial food coloring, plastic-looking food,
no texture, flat lighting, cold tones, unnatural colors,
overcooked appearance, moldy, stale-looking
```

**Для электроники:**
```
Fingerprints, smudges, scratches, damaged, outdated design,
cheap plastic, toy-like, unrealistic screen, wrong proportions
```

**Для стекла/прозрачных материалов:**
```
Opaque, cloudy, dirty, fingerprints, unrealistic refraction,
no transparency, flat appearance, missing reflections
```

---

## Чеклист перед генерацией

Перед отправкой промпта убедитесь, что указали:

✅ **Субъект:**
- [ ] Точное название продукта
- [ ] Материалы с описанием отделки (brushed, polished, matte)
- [ ] Цвет с оттенком (не просто "синий", а "navy blue")
- [ ] Состояние (новый, с конденсатом, в упаковке)

✅ **Действие/Эффекты:**
- [ ] Физические эффекты (пар, капли, брызги) или
- [ ] Позиционирование (standing, laying, tilted)

✅ **Окружение:**
- [ ] Поверхность (white seamless, marble, wood)
- [ ] Фон (infinity white, gradient, lifestyle scene)
- [ ] Контекст (студия или реальное использование)

✅ **Композиция:**
- [ ] Угол съемки (3/4 view, top-down, straight-on)
- [ ] Объектив (50mm, 85mm, 100mm macro)
- [ ] Диафрагма (f/8 для резкости, f/2.8 для боке)

✅ **Стиль:**
- [ ] Назначение (e-commerce, advertising, lifestyle)
- [ ] Освещение (studio, natural, dramatic)
- [ ] Качество (4K, high resolution, commercial quality)

✅ **Негативный промпт:**
- [ ] Добавлен список нежелательных элементов

---

## Типичные ошибки и решения

| Проблема | Причина | Решение |
|----------|---------|---------|
| Продукт выглядит "пластиковым" | Не указаны текстуры материалов | Добавить: "brushed metal texture", "visible grain", "natural imperfections" |
| Неравномерное освещение | Описание света слишком общее | Указать студийную схему: "softbox at 45 degrees, white reflector fill" |
| Весь продукт не в фокусе | Не указана диафрагма | Добавить: "f/8 to f/11, entire product in sharp focus" |
| Грязный или отвлекающий фон | Не указан тип фона | Точно указать: "pure white infinity seamless background" |
| Цвета не соответствуют реальности | Не указана цель "точная передача цвета" | Добавить: "accurate color representation for e-commerce" |
| Нет объема, плоское изображение | Отсутствие теней и света | Добавить направленное освещение с тенями для глубины |

---

**Версия:** 2.0 (Методология "5 столпов" + Виртуальная Студия)
**Обновлено:** 2026-01-06
**Базируется на:** Технический отчет "Архитектура промпт-инжиниринга Nano Banana Pro"
