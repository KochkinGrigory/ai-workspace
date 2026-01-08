# Best Practice: Презентации и слайды

Профессиональное руководство по созданию презентационных материалов с использованием методологии "Negative Space First" для Nano Banana Pro.

## Когда использовать

- Титульные слайды для PowerPoint/Keynote/Google Slides
- Фоны для контентных слайдов
- Разделители секций презентации (section dividers)
- Обложки корпоративных отчетов
- Концептуальные иллюстрации для бизнес-идей
- Вебинарные заставки и завершающие слайды

---

## Фундаментальная концепция: Negative Space First

### От декоративных фонов к функциональным слайдам

Nano Banana Pro (Gemini 3 Pro Image Preview) понимает **функциональную роль пространства** в презентациях. Модель не просто "делает красивую картинку", а **проектирует слайд с учетом будущего текстового контента**.

**Критическое различие:**

❌ **Старый подход (декоративный фон):**
```
corporate presentation background, blue, professional, modern, abstract
```

✅ **Новый подход (функциональный дизайн):**
```
Professional business presentation title slide background optimized for text overlay.
Layout Structure: 16:9 landscape format for PowerPoint.
Negative Space Allocation: Central 60% of canvas (horizontally centered, vertically
centered) kept completely clear and empty for title and subtitle text placement,
ensuring maximum 240-character title can fit comfortably.
Visual Elements: Abstract geometric pattern confined to left and right edges (15%
from each side), composed of thin navy blue lines forming subtle grid pattern,
creating professional technical aesthetic without visual clutter.
Background Treatment: Smooth gradient from light gray #F3F4F6 at top transitioning
to pure white #FFFFFF at center where text will be, ensuring maximum contrast for
dark text readability. Bottom third returns to light gray creating balanced frame.
Projection Considerations: High contrast suitable for bright conference room projection,
no fine details that would be lost on screen, color palette tested for colorblind accessibility.
Style: Corporate minimalist aesthetic, professional and undistracting, supports speaker's
message without competing for attention, timeless design suitable for formal business context.

Negative Prompt: Busy pattern in center, low contrast, decorative illustrations,
gradient text effects, small details, centered focal point blocking text area.
```

### Почему это работает для презентаций

Модель **планирует слайд как систему "контент + поддержка"** перед рендерингом:
1. Определяет приоритетные зоны для текста (где будет заголовок, подзаголовок, body)
2. Рассчитывает безопасные отступы (title-safe и action-safe зоны от проекторов)
3. Анализирует контраст фона для читаемости (темный текст требует светлого фона)
4. Понимает "визуальный вес" элементов (не перегружать края, если текст в центре)

Это означает, что вы работаете не с "дизайнером обоев", а с **презентационным архитектором**, который учитывает будущее использование слайда спикером.

---

## Пять Столпов для Презентационного Дизайна

Адаптация "5 столпов" под специфику слайдов и презентаций.

### 1. Субъект (Subject) - Тема презентации и роль слайда

**Что указывать:**
- Тип слайда: Title slide (титульный), Content background (фон для контента), Section divider (разделитель), Concept illustration (концепт)
- Тема презентации: финансовый отчет, продуктовый питч, тренинг, вебинар
- Целевая аудитория: совет директоров, клиенты, сотрудники, конференция
- Контекст использования: проектор в зале, экран вебинара, печатный буклет

**Примеры:**
- ❌ Слабо: "Слайд для презентации"
- ✅ Хорошо: "Title slide background for quarterly financial results presentation to board of directors, projected in formal boardroom setting"
- ❌ Слабо: "Фон с бизнес-концепцией"
- ✅ Хорошо: "Concept illustration slide visualizing 'Digital Transformation' for internal company training webinar, need to accommodate heading and 3 bullet points"

### 2. Действие (Action) - Визуальная поддержка сообщения

В контексте презентаций "действие" — это **как изображение усиливает послание спикера**, не конкурируя за внимание.

**Типы визуальной поддержки:**
- **Фрейминг (Framing):** "Создает визуальную рамку, направляющую взгляд к тексту в центре"
- **Усиление тона (Mood Reinforcement):** "Поддерживает серьезный/оптимистичный/инновационный тон презентации через цвет и композицию"
- **Метафорическая иллюстрация (Metaphor):** "Визуально представляет абстрактную концепцию (рост, команда, инновации)"
- **Брендинг (Branding):** "Ненавязчиво интегрирует корпоративную идентичность через цветовую палитру"
- **Разграничение секций (Separation):** "Сигнализирует переход к новому разделу презентации"

**Как описывать:**
```
Visual Support Role: This slide background serves to frame the quarterly results title
without distracting from key numbers. The upward-trending abstract lines in corners
subtly reinforce positive growth message while keeping central 70% completely empty
for speaker's data. Audience focus remains on content, not decoration.
```

### 3. Окружение (Location/Context) - Структура пространства и негативные зоны

**Критично для презентаций:** Четко определить, **где будет текст** и **где визуальные элементы**.

**Типы пространственной организации:**

**A) Center-Focused (текст в центре):**
```
Canvas: 16:9 landscape (1920x1080px minimum).
Negative Space: Central rectangle spanning 60% width × 50% height perfectly clear,
no visual elements, solid background for maximum text contrast.
Visual Elements: Confined to perimeter - decorative elements only in outer 20%
from each edge, creating natural frame around text area.
```

**B) Left-Text / Right-Visual (левый текст, правая визуализация):**
```
Canvas: 16:9 landscape.
Negative Space: Left 50% of canvas reserved for text content (title, bullets, paragraphs),
pure white or solid color background in this zone.
Visual Elements: Right 50% contains illustration, photo, or graphic supporting the topic,
subtle blur or fade at division line for seamless integration.
```

**C) Top-Heavy (текст снизу, визуал сверху):**
```
Canvas: 16:9 landscape.
Negative Space: Bottom 40% solid background for content text.
Visual Elements: Top 60% contains hero image or illustration, with gradient fade
toward bottom ensuring smooth transition to text area.
```

**D) Full-Bleed with Overlay Zones (фоновое фото с зонами для текста):**
```
Canvas: 16:9 landscape.
Background: Full-bleed photographic image across entire slide.
Overlay Zones: Semi-transparent dark boxes positioned strategically - one in top-left
quadrant for title (opacity 85% black), one in bottom-right for supporting text,
creating high-contrast zones for white text readability.
```

### 4. Композиция (Composition) - Визуальный баланс и читаемость

**Принципы организации для проекции:**

**Title-Safe и Action-Safe зоны:**
```
Projection Safety Margins: All critical content (text, logos, key visuals) positioned
minimum 10% from all edges (192px from left/right edges, 108px from top/bottom on 1920x1080).
This accounts for overscan on projectors and different screen aspect ratios.
Background elements can extend to edges but text zones must respect safe areas.
```

**Контраст для читаемости:**
```
High Contrast Zones: Areas designated for text must have minimum 7:1 contrast ratio
(WCAG AAA standard for large text, accessibility for back-row viewers).
Dark text (#1F2937 or darker) requires light background (#F9FAFB or lighter).
Light text (#FFFFFF) requires dark background (#1F2937 or darker) or overlay gradient.
```

**Визуальный вес и баланс:**
```
Asymmetric Balance: If visual element is on left (heavy), balance with negative space
on right (light). For example, bold geometric pattern left edge should be countered
by completely clean white space right side where bullet points will go.

Vertical Rhythm: If title will be top-aligned, keep visual interest in bottom third
to balance composition. If title centered, distribute decorative elements equally
top and bottom to frame it symmetrically.
```

**Градиенты для текстовых зон:**
```
Strategic Gradient Overlays: For slides with photographic backgrounds, apply directional
gradients creating solid color zones for text:
- Bottom-to-top gradient (dark #1E293B at bottom 30% fading to transparent) for
  footer text in white
- Radial gradient (darkening from center outward) creating bright center spotlight
  for title with dark edges for visual framing
```

### 5. Стиль (Style) - Визуальная эстетика и презентационный контекст

**Четыре основных эстетики:**

**Corporate/Conservative (корпоративная):**
```
Professional corporate aesthetic suitable for board presentations and formal reports,
conservative color palette (navy blue #1E3A8A, charcoal gray #374151, white),
geometric precision with clean lines, no playful elements, timeless design avoiding
trends, conveys trust and stability, appropriate for finance, legal, consulting sectors.
```

**Tech/Innovation (технологическая/инновационная):**
```
Modern tech-forward aesthetic for product launches and innovation presentations,
electric blue #3B82F6 and cyan #06B6D4 color accents, subtle gradient effects,
clean sans-serif typography implied by design, hints of depth through layering
without heavy 3D, conveys cutting-edge and forward-thinking, suitable for startups,
tech companies, digital transformation topics.
```

**Educational/Friendly (образовательная):**
```
Approachable friendly design for training and internal communications, warm colors
(orange #F97316, teal #14B8A6, soft yellow #FDE047), rounded shapes instead of
hard angles, slightly playful but still professional, inviting and non-threatening
for learning context, suitable for HR presentations, onboarding, workshops.
```

**Premium/Luxury (премиальная):**
```
High-end sophisticated aesthetic for luxury brands and premium services, dark
backgrounds (black #000000, deep navy #0F172A), metallic gold #D4AF37 or rose gold
accents, generous white space conveying exclusivity, minimal elements suggesting
refinement, subtle lighting effects creating depth, appropriate for luxury goods,
high-end consulting, exclusive services.
```

---

## Типы Презентационных Слайдов: Специфика и Промпты

### Тип 1: Title Slide (Титульный слайд)

**Назначение:** Первый слайд презентации, представляет тему и спикера

**Требования:**
- Максимальная визуальная привлекательность (first impression)
- Пространство для: заголовок (1-2 строки), подзаголовок, дата, имя спикера, логотип компании
- Профессиональный tone, соответствующий важности презентации

**Промпт-пример:**
```
Professional corporate title slide background for quarterly business review presentation.

Subject: Q4 2025 Financial Results presentation to executive leadership team,
projected in main boardroom on large screen.

Visual Support: Design creates prestigious first impression while maintaining focus
on presentation title. Abstract elements suggest financial growth without literal
charts, allowing numbers to be revealed later in deck. Conservative aesthetic
appropriate for C-suite audience.

Layout Structure:
Canvas: 16:9 landscape format (1920x1080px).

Negative Space Allocation:
- Top 15%: Clear area for company logo (top-left corner)
- Central 50% (both horizontally and vertically): Completely empty zone for
  presentation title 'Q4 2025 FINANCIAL RESULTS' (estimated 80pt text) and
  subtitle 'Board of Directors Review' (40pt text)
- Bottom 10%: Clear zone for presenter name and date

Visual Elements Placement:
- Bottom-right corner (25% of slide area): Abstract geometric composition of
  ascending bars/lines in subtle navy blue #1E3A8A suggesting upward trend,
  semi-transparent (60% opacity) to remain unobtrusive
- Top-right corner (10% area): Complementary minimal geometric accent balancing
  bottom element

Background Treatment:
- Base: Clean white #FFFFFF across 70% of slide for maximum text contrast
- Gradient overlay: Very subtle light gray #F3F4F6 vignette at edges (10% opacity)
  creating soft framing effect without reducing text readability

Projection Optimization:
- All visual elements maintain 10% safe margin from edges (title-safe zone)
- High contrast ensured for 100+ people audience viewing from back of room
- No fine details smaller than 20px that would be lost on projection

Typography Implied: Sans-serif bold for title, regular weight for subtitle,
high contrast dark navy text on white background.

Style: Modern corporate professional, minimalist with purpose, conveys competence
and success through clean execution, timeless design avoiding trendy elements,
suitable for printing in annual report if needed.

Negative Prompt: Busy patterns in center, low contrast gradients, decorative
illustrations, stock photos of people, centered visual blocking text placement,
playful elements, bright colors, anything distracting from title text.
```

### Тип 2: Content Slide Background (Фон для контентного слайда)

**Назначение:** Повторяющийся фон для слайдов с текстовым контентом, bullet points, данными

**Требования:**
- Максимально ненавязчивый (не отвлекает от контента)
- Поддерживает визуальную связь с титульным слайдом (единство стиля)
- Пространство для: заголовок слайда, 3-5 bullet points или параграфы, footer
- Повторяется на 80% слайдов презентации

**Промпт-пример:**
```
Subtle content slide background for business presentation, designed for repeated use.

Subject: Standard content slide background for sales pitch deck, will host bullet
points, data, and speaker notes across 40+ slides in presentation.

Visual Support: Provides minimal visual interest to prevent "plain white slide fatigue"
while remaining completely unobtrusive. Reinforces brand colors subtly without
competing with slide content. Viewer focus stays 100% on text and data.

Layout Structure:
Canvas: 16:9 landscape.

Negative Space Allocation:
- Entire canvas (95%) must be usable for content - virtually complete availability
- Top 20%: Reserved for slide heading/title
- Middle 60%: Main content area for bullets, text, charts
- Bottom 10%: Footer area for page numbers, confidential notices

Visual Elements Placement:
- Bottom-right corner ONLY: Tiny (3% of slide) abstract geometric mark in brand
  blue #2563EB at 30% opacity, purely decorative accent not readable detail
- Thin (2px) accent line along bottom edge in same blue, running 80% width
  (respecting safe margins)
- NO other visual elements anywhere else

Background Treatment:
- Pure white #FFFFFF base across entire slide for maximum text versatility
- Extremely subtle (5% opacity) light gray #F9FAFB texture in top-right quadrant
  only, adding microscopic visual interest without being noticeable

Projection Optimization:
- Zero contrast issues - white background works with any text color
- Geometric mark too small to distract but visible enough to prevent "generic" feel
- Suitable for 200+ slide presentations without causing visual fatigue

Style: Ultra-minimalist corporate, designed to disappear while maintaining brand
presence, professional and clean, timeless design usable for years of presentations.

Negative Prompt: Any prominent visual elements, patterns, gradients, illustrations,
photos, colors in content area, centered graphics, decorative borders, anything
noticeable that would compete with slide content.
```

### Тип 3: Section Divider (Разделитель секций)

**Назначение:** Сигнализирует переход к новому разделу презентации

**Требования:**
- Визуально отличается от content slides (привлекает внимание к смене темы)
- Пространство для: название секции (1-3 слова)
- Более смелый дизайн чем content slides, но не перегруженный

**Промпт-пример:**
```
Section divider slide for corporate presentation marking transition to new topic.

Subject: Divider slide separating 'Market Analysis' section from 'Product Strategy'
section in strategic planning presentation, provides visual break between dense
content sections.

Visual Support: Creates clear mental break for audience, refreshing attention after
20+ content slides. Bold enough to signal "new chapter" but maintains presentation's
professional tone. Prepares audience for topic shift.

Layout Structure:
Canvas: 16:9 landscape.

Negative Space Allocation:
- Central horizontal band (60% width × 30% height centered): Solid color block
  for section title text 'PRODUCT STRATEGY' in white, completely clear internally
- Remaining 70% of slide: Background treatment

Visual Elements:
- Left side: Abstract gradient wash from brand blue #2563EB (saturated at left edge)
  fading to transparent at 40% width mark, creating color sweep effect
- Right side: Mirror gradient from brand orange #F97316 (saturated at right edge)
  fading to transparent at 60% width mark
- Center: Gradients meet and overlap creating neutral zone behind title block

Background Treatment:
- Base: White #FFFFFF showing through in center where gradients fade
- Title block: Solid navy #1E293B rectangle with crisp edges, providing high-contrast
  platform for white section title text

Visual Effect: Color sweeps from sides feel dynamic and directional, suggesting
forward movement into new section, while center remains clean and focused on text.

Typography Implied: Section title in all-caps bold sans-serif white text, large
(72pt equivalent), centered in navy block.

Style: Modern corporate with dynamic energy, more visually bold than content slides
but still professional, color usage is justified (marking important transition) not
decorative, suitable for formal business context.

Negative Prompt: Centered busy visuals, low contrast, decorative illustrations,
photos, excessive colors, gradient text, anything competing with section title,
playful elements inappropriate for serious business presentation.
```

### Тип 4: Concept Illustration Slide (Концептуальная иллюстрация)

**Назначение:** Визуализирует абстрактную бизнес-концепцию (teamwork, growth, innovation)

**Требования:**
- Легко понимаемая визуальная метафора
- Профессиональное исполнение (не clip-art)
- Может занимать больше пространства чем background slides
- Поддерживает спикера, не заменяет объяснение

**Промпт-пример:**
```
Concept illustration slide visualizing 'Digital Transformation' for business presentation.

Subject: Full slide visual metaphor explaining digital transformation concept for
technology strategy presentation to non-technical executives, needs to communicate
"traditional business evolving to digital-first" clearly and memorably.

Visual Support: Provides concrete visual anchor for abstract concept, helping audience
understand and remember key message. Designed to support 2-3 minutes of speaker
explanation, reinforcing talking points about organizational change.

Layout Structure:
Canvas: 16:9 landscape.

Visual Composition:
Left Half (40% of canvas):
- Illustration of traditional office elements: filing cabinet, landline phone,
  paper documents, rendered in grayscale tones (#6B7280) with slight fading
  (70% opacity) suggesting "old way"
- Subtle dotted outline suggesting these elements are dissolving/transitioning

Center (20% of canvas):
- Large rightward-pointing arrow, composed of glowing particle effect in gradient
  blue-to-purple (#3B82F6 to #8B5CF6), suggesting transformation in progress
- Arrow contains small icons representing change: cloud, mobile, AI symbols

Right Half (40% of canvas):
- Illustration of digital workplace: laptop, smartphone, cloud icons, dashboard
  interfaces, rendered in full-color vibrant blues and cyans, appearing solid
  and forward-facing suggesting "new way"
- Modern, tech-forward aesthetic

Background Treatment:
- Clean white #FFFFFF base for maximum clarity of visual metaphor
- Subtle light gray grid pattern (#F3F4F6 at 10% opacity) in background suggesting
  structured organizational framework

Text Zones:
- Top 15%: Clear space for slide title 'EMBRACING DIGITAL TRANSFORMATION'
- Bottom 15%: Optional space for 1-2 bullet points highlighting key benefits

Projection Optimization:
- Bold shapes and high contrast for visibility from back of 200-person auditorium
- Color differentiation clear even for colorblind viewers (grayscale left vs. saturated right)
- No text within illustration itself, all labels would be separate overlay

Style: Professional business illustration, clean vector-style artwork (not photorealistic,
not cartoon), similar to McKinsey/BCG consulting presentation aesthetics, modern but
not trendy, timeless design appropriate for C-suite audience.

Negative Prompt: Cartoon characters, literal photographs, stock clip-art, overly
complex diagram, small text labels, realistic 3D rendering, playful mascots,
anything unprofessional or difficult to understand at a glance.
```

---

## Цветовые палитры по отраслям и контексту

### Финансовые услуги (Banking, Insurance, Investment)
```
Primary: Dark blue #1E40AF (trust, stability)
Secondary: Gold #D97706 (premium, value)
Accent: Forest green #047857 (growth, money)
Neutral: Charcoal #374151, White #FFFFFF

Psychology: Conservative, trustworthy, established, communicates security of assets
```

### Технологии и SaaS (Tech, Software, Startups)
```
Primary: Electric blue #3B82F6 (innovation, digital)
Secondary: Cyan #06B6D4 (cutting-edge, cloud)
Accent: Purple #8B5CF6 (creative, future-focused)
Neutral: Slate gray #64748B, White #FFFFFF

Psychology: Modern, innovative, forward-thinking, suggests digital transformation
```

### Здравоохранение и медицина (Healthcare, Pharma, Wellness)
```
Primary: Medical blue #0EA5E9 (clinical, clean)
Secondary: Mint green #10B981 (health, growth, care)
Accent: Soft coral #FB923C (warmth, human touch)
Neutral: Light gray #E5E7EB, White #FFFFFF

Psychology: Clean, caring, professional, trustworthy medical expertise
```

### Консалтинг и профессиональные услуги (Consulting, Legal, Advisory)
```
Primary: Navy #1E3A8A (authority, expertise)
Secondary: Burgundy #991B1B (seriousness, premium)
Accent: Steel blue #475569 (professional, analytical)
Neutral: Warm gray #78716C, Cream #FFFBEB

Psychology: Authoritative, serious, expert, commands respect and trust
```

### Образование и тренинг (Education, Training, HR)
```
Primary: Teal #14B8A6 (growth, learning)
Secondary: Orange #F97316 (energy, enthusiasm)
Accent: Yellow #FDE047 (optimism, ideas)
Neutral: Soft gray #9CA3AF, White #FFFFFF

Psychology: Approachable, energetic, positive, encourages learning and engagement
```

---

## Негативные промпты для презентаций

**Универсальный негативный промпт:**
```
Busy center area, low contrast for text, decorative elements in text zones,
small intricate details lost on projection, gradients reducing readability,
centered focal point blocking title placement, clip-art quality, unprofessional
aesthetics, trendy design elements aging quickly, bright neon colors, comic sans,
personal/casual tone inappropriate for business, missing safe margins, elements
too close to edges, fine text within graphics, aspect ratio other than 16:9
```

**Для формальных презентаций (совет директоров, инвесторы):**
```
Playful elements, casual aesthetics, cartoon style, bright saturated colors,
rounded bubbly shapes, informal tone, trendy design, anything suggesting
unprofessionalism or lack of seriousness
```

**Для концептуальных слайдов:**
```
Confusing metaphors, unclear symbolism, multiple conflicting concepts,
overly abstract without clear meaning, complex diagrams, text-heavy
explanations within illustration, realistic photos when metaphor needed
```

**Для title slides:**
```
Visuals competing with title text, low contrast backgrounds, centered
graphics, decorative fonts implied, busy patterns, anything distracting
from first impression of professionalism
```

---

## Чеклист перед генерацией

✅ **Тип слайда:**
- [ ] Определен тип (title/content/divider/concept)
- [ ] Понятно назначение слайда в презентации
- [ ] Определен объем текста для размещения

✅ **Negative Space:**
- [ ] Четко указаны зоны для текста (процент от слайда)
- [ ] Указано расположение (центр/лево/право/верх/низ)
- [ ] Обеспечены title-safe margins (10% от краев)

✅ **Контраст и читаемость:**
- [ ] Определен цвет будущего текста (темный/светлый)
- [ ] Фон в текстовых зонах обеспечивает контраст 7:1
- [ ] Нет мелких деталей, теряющихся при проекции

✅ **Визуальные элементы:**
- [ ] Расположены ВНЕ текстовых зон
- [ ] Не конкурируют за внимание с контентом
- [ ] Поддерживают тему презентации

✅ **Технические параметры:**
- [ ] Формат 16:9 (или указан другой)
- [ ] Разрешение min 1920x1080
- [ ] Цветовая палитра соответствует отрасли/бренду

✅ **Стиль и тон:**
- [ ] Соответствует аудитории (C-suite/клиенты/сотрудники)
- [ ] Профессиональный уровень (не декоративный, не clip-art)
- [ ] Согласуется с контекстом (формальный/неформальный)

✅ **Негативный промпт:**
- [ ] Добавлены запреты на типичные проблемы

---

## Типичные ошибки и решения

| Проблема | Причина | Решение |
|----------|---------|---------|
| Текст не помещается на слайде | Недостаточно negative space | Явно указать: "central 60% completely empty for title up to 240 characters" |
| Низкая читаемость при проекции | Слабый контраст | Обеспечить: "minimum 7:1 contrast, dark #1F2937 text on light #F9FAFB background" |
| Визуалы отвлекают от контента | Элементы в центре внимания | Переместить: "all decorative elements confined to outer 20% edge zones only" |
| Слайды выглядят разрозненно | Нет единого стиля | Создать систему: "consistent color palette across all slide types, unified geometric language" |
| Потеря деталей на проекторе | Мелкие элементы | Упростить: "no details smaller than 20px, bold shapes only, high contrast" |
| Непрофессиональный вид | Декоративность вместо функциональности | Минимализм: "every element serves purpose, remove decoration, clean professional execution" |

---

**Версия:** 2.0 (Методология "Negative Space First" + Projection Optimization)
**Обновлено:** 2026-01-06
**Базируется на:** Технический отчет "Архитектура промпт-инжиниринга Nano Banana Pro"
