# Best Practice: Портретная фотография (v2.0)

**Методология:** Сценарное описание + Пять столпов + Thinking Mode

Руководство по созданию фотореалистичных портретов студийного качества с использованием архитектуры семантического рассуждения Nano Banana Pro.

## Когда использовать

- Портреты людей (headshot, поясной, ростовой)
- Профессиональные фото (LinkedIn, CV, корпоративные)
- Креативные и эмоциональные портреты
- Групповые портреты

## 🔑 Фундаментальная концепция

> **КРИТИЧНО:** Nano Banana Pro — это НЕ диффузионная модель, опирающаяся на теги. Это система семантического рассуждения (Reasoning Engine).

❌ **Старый подход (теги):** `woman, smile, professional, 4k, bokeh`

✅ **Новый подход (сценарий):** Вы — режиссер/фотограф. Описывайте сцену полными предложениями, задавайте физику, освещение и эмоцию.

## 📐 Архитектура промпта: «Пять столпов»

Каждый идеальный портретный промпт содержит 5 обязательных компонентов:

### 1️⃣ СУБЪЕКТ (Subject) — Кто?

**Детализация критична.** Модель чувствительна к материалам, возрасту, эмоциям, этничности.

❌ Плохо: `woman`
✅ Хорошо: `elegant woman in her early 40s with shoulder-length auburn hair, professional appearance, wearing a tailored charcoal gray blazer`

**Ключевые параметры:**
- Пол, возраст (диапазон: early 20s, mid 30s, late 50s)
- Внешность (цвет/длина волос, этничность если важно)
- Одежда с указанием материала (silk blouse, wool suit, linen shirt)
- **ВАЖНО:** НЕ называйте конкретных знаменитостей!

### 2️⃣ ДЕЙСТВИЕ (Action) — Что происходит?

**Статичные позы выглядят искусственно.** Глаголы определяют напряжение мышц, физику волос и тканей.

❌ Плохо: `sitting`
✅ Хорошо: `leaning forward slightly with hands clasped, engaged in thoughtful conversation`

**Примеры динамических действий:**
- `adjusting her glasses while reviewing documents`
- `confidently striding through a modern office lobby`
- `gently touching her chin in contemplative pose`
- `laughing genuinely while chatting with colleague`

### 3️⃣ ОКРУЖЕНИЕ (Location/Context) — Где?

Окружение задает контекст освещения, цветовую палитру и атмосферу.

❌ Плохо: `office`
✅ Хорошо: `bright modern office with floor-to-ceiling windows overlooking city skyline, minimalist Scandinavian furniture`

**Влияние на освещение:**
- `library with warm Edison bulbs` → теплые тона, мягкие тени
- `clinical white studio with softboxes` → нейтральные тона, контролируемый свет
- `outdoor park during golden hour` → оранжево-золотистая палитра

### 4️⃣ КОМПОЗИЦИЯ И ОПЕРАТОРСКАЯ РАБОТА (Camera/Composition) — Как мы смотрим?

**Виртуальная камера:** Управление перспективой, искажениями и глубиной резкости.

#### Фокусное расстояние (Focal Length)

| Объектив | Применение | Эффект |
|----------|------------|--------|
| **85mm** | Классический портрет | Сжимает пространство, комплиментарно для лица, золотой стандарт |
| **50mm** | Естественная перспектива | Близко к человеческому глазу, универсал |
| **135mm** | Телефото-портрет | Сильное сжатие, драматичное боке |
| **35mm** | Контекстный портрет | Показывает окружение вокруг героя |
| **100mm Macro** | Экстрим крупный план | Текстура кожи, глаза, детали |

#### Диафрагма (Aperture) и Глубина резкости

| Диафрагма | Эффект | Применение |
|-----------|--------|------------|
| **f/1.2 - f/2.0** | Экстремально малая глубина резкости, сливочное боке | Художественные портреты, отделение от фона |
| **f/2.8 - f/4** | Умеренная глубина резкости | Профессиональные headshots, баланс резкости и боке |
| **f/5.6 - f/8** | Большая глубина резкости | Групповые портреты (все лица в фокусе) |

**Синтаксис:**
```
Shot on [camera body] with [lens focal length] lens, aperture [f-stop],
[focus point], [bokeh characteristic]
```

**Примеры:**
- `Shot on Hasselblad medium format camera, 80mm f/2.8 lens, sharp focus on eyes, creamy bokeh background`
- `Shot on Canon 5D Mark IV, 85mm f/1.4 lens, extremely shallow depth of field, subject isolated from background`

#### Ракурсы и углы

- `eye-level angle` — стандарт, равноправие
- `shot from slightly above` — стройнит, сужает лицо
- `low angle shot` — монументальность, power pose
- `Dutch angle (tilted)` — динамика, неформальность

### 5️⃣ СТИЛЬ (Style) — Какова эстетика?

Определяет визуальный язык и постобработку.

**Для фотореализма:**
- `Hyperrealistic photography` / `Photorealistic professional photography`
- `Editorial style for [Vogue/National Geographic/GQ]`
- `Unedited RAW file aesthetic` / `Minimal retouching`
- `High-end commercial photography`

**Ключевые слова качества:**
- `8K resolution`, `High resolution`, `Ultra-detailed`
- `Professional quality`, `Studio-grade`

## 💡 Сценарии освещения (Lighting Scenarios)

Свет формирует объем и настроение. Используйте специфические типы, НЕ общие слова.

### Студийное освещение

**Rembrandt Lighting** (Рембрандтовский свет):
```
Classic Rembrandt lighting setup: Key light at 45-degree angle creating
characteristic light triangle on shadow side of face, dramatic chiaroscuro effect
```
- **Эффект:** Световой треугольник на щеке, объем, драматизм
- **Применение:** Мужские портреты, характерные лица

**Softbox / Beauty Lighting:**
```
Soft diffused studio lighting with large octagonal softbox positioned directly
in front, eliminating harsh shadows, beauty dish effect
```
- **Эффект:** Равномерный мягкий свет без жестких теней
- **Применение:** Бьюти-съемка, гламурные портреты, косметика

**Three-Point Lighting:**
```
Classic three-point lighting: Key light from 45 degrees, fill light opposite
to soften shadows, rim light from behind creating separation from background
```
- **Эффект:** Профессиональный, контролируемый студийный свет
- **Применение:** Корпоративные headshots, интервью

### Естественное освещение

**Golden Hour:**
```
Photographed during golden hour, low warm sunlight creating soft orange-golden
glow on skin, long gentle shadows, flattering natural light
```
- **Эффект:** Теплые тона, романтичность, мягкие тени
- **Применение:** Лайфстайл, свадебные портреты

**Blue Hour:**
```
Shot during blue hour twilight, deep cool blue ambient light, mysterious
and contemplative atmosphere
```
- **Эффект:** Холодная синяя палитра, меланхолия
- **Применение:** Концептуальные, эмоциональные портреты

**Soft Window Light:**
```
Soft natural light streaming through large window from left side,
creating gentle gradient of shadows across face, north-facing window quality
```
- **Эффект:** Мягкие переходы, естественность
- **Применение:** Домашние, интимные портреты

### Специальные эффекты освещения

**Rim Lighting / Backlighting:**
```
Strong rim light from behind subject creating luminous halo effect,
separating dark subject from dark background, edge lighting
```
- **Эффект:** Светящийся контур вокруг силуэта
- **Применение:** Драматичные, кинематографичные портреты

**Volumetric Lighting / God Rays:**
```
Volumetric light beams cutting through atmospheric haze,
dust particles visible in light shafts, dramatic god rays effect
```
- **Эффект:** Лучи света в тумане/дыму, эпичность
- **Применение:** Концептуальные, художественные портреты

## 🔬 Материальность и текстура (КРИТИЧНО для фотореализма!)

> **Проблема ИИ:** "Пластиковая" кожа без текстуры.
> **Решение:** Явно запрашивайте несовершенства и текстурные детали.

### Обязательные ключевые слова для реализма:

```
Natural skin texture visible, skin pores clearly defined, subtle freckles,
fine vellus hair (peach fuzz) on face, minor skin imperfections,
subsurface scattering on skin, realistic skin translucency,
individual eyelashes, detailed iris structure, catchlight in eyes
```

**Расшифровка:**
- `Skin texture` / `Visible pores` — текстура кожи, поры
- `Freckles` — веснушки
- `Vellus hair` / `Peach fuzz` — пушковые волосы на лице
- `Imperfections` / `Minor blemishes` — несовершенства, естественные дефекты
- `Subsurface scattering` — подповерхностное рассеивание света (просвечивание кожи/ушей)
- `Catchlight in eyes` — отражение источника света в глазах (блик)

### Негативный промпт (Negative Prompt)

**Обязательно используйте** для устранения типичных артефактов:

```
Negative: cartoon, illustration, painting, drawing, 3D render, CGI,
overly smooth skin, plastic skin, artificial looking, airbrushed,
bad quality, low resolution, blur, distortion, deformed hands,
mutated hands, extra fingers, extra limbs, watermark, text, signature
```

## 📋 Примеры промптов по типам

### 1. Профессиональный Headshot (LinkedIn, CV)

```
Hyperrealistic professional headshot of a confident business executive,
male in his mid-40s with salt-and-pepper hair neatly styled.
Action: He is making direct eye contact with camera, displaying
a warm yet authoritative smile.
Clothing: Wearing impeccably tailored navy blue suit with crisp white shirt
and burgundy silk tie.
Environment: Shot in modern corporate office with neutral gray seamless
background, subtle gradient lighting.
Camera: Shot on Hasselblad H6D medium format camera with 80mm f/2.8 lens,
aperture set to f/4 for optimal sharpness across entire face.
Lighting: Classic three-point lighting setup with large octagonal softbox
as key light from 45 degrees, creating gentle modeling on face,
fill light opposite to open shadows, subtle rim light from behind
for separation.
Details: Natural skin texture visible with pores clearly defined,
individual gray hairs in stubble, catchlight in eyes from softbox,
sharp focus on eyes extending to ears, creamy bokeh background.
Style: Editorial corporate photography for Fortune 500 annual report,
minimal retouching maintaining natural character, professional color grading
with slight cool tone, 8K resolution.

Negative Prompt: cartoon, illustration, overly smooth skin, plastic appearance,
artificial, bad quality, deformed features, watermark
```

### 2. Креативный художественный портрет

```
Cinematic portrait of a young female artist in her late 20s with vibrant
red-orange hair in loose messy bun.
Action: She is leaning against her studio wall, one hand gently touching
her paint-stained denim apron, gazing pensively toward large industrial window.
Environment: Bright art studio loft with exposed brick walls, large
north-facing windows flooding space with diffused daylight, colorful
abstract paintings on easels visible but softly blurred in background,
scattered brushes and paint tubes on wooden table.
Camera: Shot on Canon EOS R5 with 50mm f/1.2 lens, aperture wide open at f/1.2
creating extremely shallow depth of field, sharp focus locked on her closest eye,
everything else melting into creamy bokeh.
Lighting: Soft natural window light from left creating gentle Rembrandt lighting
pattern with characteristic light triangle on right cheek, golden hour warm glow
filtering through gauze curtains, subtle rim light from window behind creating
luminous halo on hair edges.
Details: Visible skin texture with freckles across nose and cheeks,
individual strands of loose hair catching backlight, paint smudges on hands,
vellus hair on face, subsurface scattering making ear glow translucent,
green eyes with detailed iris and catchlight reflection of window,
natural minor imperfections.
Style: Editorial photography for art magazine, intimate and contemplative mood,
warm color grading with golden tones, shot on Kodak Portra 400 film aesthetic,
high resolution unedited RAW, photorealistic, professional quality.

Negative Prompt: cartoon, illustration, 3D render, overly smooth skin,
airbrushed, artificial, bad anatomy, extra fingers, watermark
```

### 3. Эмоциональный портрет с глубиной

```
Deeply emotional close-up portrait of an elderly grandmother in her 70s.
Action: She is sitting in her favorite armchair by window, gently wiping
a tear of joy from her eye while holding an old family photograph in her other hand,
genuine smile breaking through tears.
Appearance: Silver-white hair pulled back in soft bun, wearing soft beige
cashmere cardigan over floral dress, weathered hands showing life experience,
laugh lines around eyes.
Environment: Cozy living room with vintage furniture, late afternoon sunlight
streaming through lace curtains, family photos on mantelpiece softly blurred
in background.
Camera: Shot on Sony A7R V with 105mm f/1.4 lens at f/2.0 aperture,
macro-level detail, razor-sharp focus on her eyes with tears glistening,
shallow depth of field isolating her face from surroundings.
Lighting: Soft warm natural light from window positioned at 90-degree angle,
creating gentle side lighting that accentuates facial contours and wrinkles
with dignity, golden late afternoon quality, subtle fill from room's ambient light.
Details: Hyper-detailed skin texture showing every wrinkle and age spot as
marks of wisdom, moisture in eyes catching light, individual white eyelashes,
fine lines around mouth, vellus hair on face, subsurface scattering on ears,
natural liver spots on hands, tears with realistic refraction.
Style: Photojournalistic documentary photography, National Geographic editorial
quality, intimate and tender mood, warm nostalgic color grading,
unedited authenticity, celebrating aging with dignity, 8K resolution.

Negative Prompt: smooth skin, artificial, overly retouched, cartoon,
illustration, fake tears, plastic appearance, bad quality, watermark
```

### 4. Групповой корпоративный портрет

```
Professional corporate team portrait of five business executives.
Composition: Arranged in casual yet organized formation - three standing
in back row (two men, one woman), two sitting on modern office chairs in front
(one man, one woman), not in rigid straight line but natural conversational positions.
Action: Team members displaying genuine camaraderie - some making eye contact
with camera with confident smiles, others glancing at colleagues mid-conversation,
relaxed but professional body language.
Appearance: Mix of ages (30s-50s) and diversity, all in business formal attire -
dark suits for men, professional blazers and dresses for women in coordinated
navy and gray palette.
Environment: Modern corporate boardroom with floor-to-ceiling windows showing
city skyline background, contemporary furniture, minimalist Scandinavian design,
company logo subtly visible on glass wall.
Camera: Shot on Canon EOS-1D X Mark III with 35mm f/1.4 lens at f/5.6 aperture
ensuring all faces remain in sharp focus across depth of group, eye-level angle.
Lighting: Balanced three-point studio lighting with large softboxes positioned
to evenly illuminate all faces, eliminating harsh shadows, fill light from reflectors,
natural window light mixing with studio lights for realistic atmosphere,
no hot spots or underexposed faces.
Details: Each face showing natural skin texture, individual characteristics
preserved, realistic expressions varying slightly, professional but approachable vibe,
visible fabric texture on suits.
Style: High-end corporate photography for company annual report, professional
color grading with slight cool corporate tone, editorial quality,
clean and polished but authentic, 8K resolution.

Negative Prompt: cartoon, illustration, plastic skin, overly airbrushed,
awkward poses, unnatural smiling, bad lighting with harsh shadows on faces,
some faces out of focus, watermark
```

## 🎨 Цветовая палитра и Color Grading

### Профессиональные/Корпоративные портреты
```
Professional color grading with slight cool tone, desaturated background
maintaining focus on subject, corporate blue and gray palette
```

### Креативные/Художественные портреты
```
Warm color grading with golden hour tones, enhanced oranges and teals
for cinematic look, slightly increased saturation for emotional impact
```

### Эмоциональные/Интимные портреты
```
Soft nostalgic color grading reminiscent of Kodak Portra film,
warm beige and cream tones, muted pastels, gentle contrast
```

## ⚠️ Типичные ошибки и решения

| ❌ Ошибка | ✅ Исправление |
|-----------|---------------|
| `woman, smile, office` (теги) | `Confident businesswoman in her 30s smiling warmly while adjusting her laptop in bright modern office` (сценарий) |
| `good lighting` (абстрактно) | `Soft window light from left creating Rembrandt lighting pattern, golden hour warmth` (конкретно) |
| Отсутствие текстуры | `visible skin pores, natural freckles, vellus hair, minor imperfections` (реализм) |
| Статичная поза | `leaning forward in engaged conversation, hands expressively gesturing` (действие) |
| Нет упоминания камеры | `Shot on Hasselblad 80mm f/2.8, aperture f/4, sharp focus on eyes` (технические параметры) |

## 📚 Технический глоссарий

**Bokeh** — художественное размытие фона
**Shallow depth of field** — малая глубина резкости (фон размыт)
**Deep depth of field** — большая глубина резкости (все в фокусе)
**Catchlight** — блик в глазах от источника света
**Chiaroscuro** — резкий контраст света и тени
**Subsurface scattering** — подповерхностное рассеивание света (просвечивание кожи)
**Vellus hair** — пушковые волосы на лице
**Rim light** — контровой свет, создающий светящийся контур
**Volumetric lighting** — объемный свет (лучи в тумане/пыли)

## 🔗 Дополнительные ресурсы

- [Официальный гайд Google Gemini](https://ai.google.dev/gemini-api/docs/image-generation)
- Схемы студийного освещения: Rembrandt, Butterfly, Loop, Split
- Референсы: "professional portrait photography Hasselblad", "editorial headshot"

---

**Версия:** 2.0 (Обновлено согласно методологии Reasoning Engine)
**Дата обновления:** 2026-01-06
**Источник методологии:** Исчерпывающий технический отчет по архитектуре промпт-инжиниринга Nano Banana Pro
