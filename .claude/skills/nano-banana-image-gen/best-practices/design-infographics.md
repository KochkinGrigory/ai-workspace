# Best Practice: Инфографика и визуализация данных

Профессиональное руководство по созданию информационной графики с использованием методологии "Structure-First" для Nano Banana Pro.

## Когда использовать

- Визуализация статистики и бизнес-метрик
- Образовательные материалы и объяснения концепций
- Пошаговые инструкции (how-to guides)
- Сравнительные таблицы и анализ
- Временные шкалы (timeline) и хронология
- Диаграммы процессов и воронки (funnels)
- Презентационные слайды с данными

---

## Фундаментальная концепция: Structure-First Design

### От визуальных тегов к логике макета

Nano Banana Pro (Gemini 3 Pro Image Preview) использует **Reasoning Engine** для понимания **логической структуры информации**, а не просто визуального стиля. Модель не "рисует красивые картинки с графиками", а **выстраивает информационную архитектуру**.

**Критическое различие:**

❌ **Старый подход (визуальные теги):**
```
infographic, statistics, blue and orange, modern, icons, clean design
```

✅ **Новый подход (структурная логика):**
```
Statistical infographic about AI market growth.
Layout Structure: Divide canvas into header section and three vertical columns.
Header: Title 'AI MARKET GROWTH 2026' in bold sans-serif, centered, dark blue color.
Column 1: Bar chart showing revenue increase from 2020-2026, vertical bars in
ascending heights, blue gradient fill, y-axis labeled '$ Billion', x-axis showing years.
Column 2: Pie chart displaying market segments - Healthcare 35%, Finance 28%,
Retail 22%, Other 15%, each segment different color with percentage label inside.
Column 3: Three key statistics as large numbers - '67%' with label 'Efficiency Gain',
'45B' with label 'Market Value', '230%' with label 'Growth Rate', stacked vertically.
Background: Clean white with subtle light gray grid pattern.
Typography: Sans-serif throughout, headings in bold weight 700, body text weight 400.
Color palette: Primary blue #2563EB, accent orange #F59E0B, neutral gray #64748B.
Style: Modern flat design, no shadows, crisp edges, professional business aesthetic.

Negative Prompt: Cluttered layout, decorative elements, gradients on background,
3D effects, illegible text, cartoon style.
```

### Почему это работает

Модель **планирует информационную иерархию** перед рендерингом:
1. Анализирует логические связи между элементами (заголовок → подразделы → детали)
2. Понимает зависимости данных (процент должен быть внутри сектора диаграммы)
3. Рассчитывает читаемость текста (контраст, размер шрифта, расстояние)
4. **Генерирует связный текст** - может писать заголовки, лейблы, числа в контексте

Это означает, что вы работаете не с "дизайнером-декоратором", а с **информационным архитектором**, которому нужно объяснить структуру и иерархию данных.

---

## Пять Столпов для Инфографики

Адаптация "5 столпов" под специфику информационного дизайна.

### 1. Субъект (Subject) - Тема и данные

**Что указывать:**
- Точная формулировка темы (не просто "статистика", а "статистика роста рынка ИИ 2020-2026")
- Тип данных: проценты, абсолютные числа, категории, временные ряды
- Ключевое сообщение: что должен понять зритель?
- Целевая аудитория: бизнес, образование, наука, маркетинг

**Примеры:**
- ❌ Слабо: "Инфографика про здоровье"
- ✅ Хорошо: "Educational infographic explaining the 5 stages of sleep cycle with brain wave patterns and duration for each stage"
- ❌ Слабо: "График продаж"
- ✅ Хорошо: "Quarterly revenue comparison Q1-Q4 2025 showing 34% growth, bar chart format with exact dollar values labeled"

### 2. Действие (Action) - История данных

В контексте инфографики "действие" — это **информационный нарратив**: какую историю рассказывают данные?

**Типы нарративов:**
- **Сравнение:** "Показывает превосходство варианта A над вариантом B"
- **Тренд:** "Демонстрирует постоянный рост с 2020 по 2025"
- **Процесс:** "Объясняет последовательность из 5 шагов от начала к результату"
- **Проблема → Решение:** "Иллюстрирует, как продукт решает три ключевые боли клиента"
- **Иерархия:** "Показывает структуру приоритетов от критичного к второстепенному"

**Как описывать:**
```
Data Story: This infographic demonstrates the dramatic increase in remote work
adoption from 2019 (18% of workforce) to 2025 (67% of workforce), showing
correlation with productivity metrics that increased by 23% over same period.
Visual flow guides viewer from problem statement (office inefficiency) through
data evidence to conclusion (hybrid model recommendation).
```

### 3. Окружение (Location/Context) - Структура макета

**Три уровня структуры:**

**A) Canvas Layout (общая композиция):**
```
Vertical infographic, portrait 9:16 ratio, suitable for Instagram Stories
Horizontal infographic, landscape 16:9 ratio, optimized for presentation slides
Square format 1:1, designed for social media feed posts
```

**B) Section Division (деление на зоны):**
```
Divide canvas into three main zones:
- Header section (top 15%): Title and subtitle
- Content area (middle 70%): Main data visualization
- Footer section (bottom 15%): Source attribution and call-to-action

OR

Grid layout with 2x2 structure:
- Top-left: Statistic 1 with icon
- Top-right: Statistic 2 with icon
- Bottom-left: Statistic 3 with icon
- Bottom-right: Statistic 4 with icon
```

**C) Background Environment:**
```
Clean white background (for maximum readability and professional appearance)
Subtle light gray (#F3F4F6) background with white content cards
Gradient background from blue to purple with white text overlay
```

### 4. Композиция (Composition) - Layout Logic

**Критически важно для Nano Banana Pro:** Описывать **логическую структуру**, а не просто "расставить элементы".

**Принципы организации:**

**Вертикальная иерархия (сверху вниз):**
```
Information flows vertically from top to bottom in logical sequence:
1. Main title at top (largest text, bold)
2. Introductory paragraph explaining context
3. Three main data points stacked vertically, each with:
   - Section heading
   - Visual element (chart/icon)
   - Supporting text
4. Conclusion summary at bottom
5. Source citation and logo in footer

Visual weight decreases from top to bottom, guiding eye naturally.
```

**Горизонтальная компоновка (слева направо):**
```
Three-column layout with equal-width columns:
Left column: 'Before' scenario with problems listed, red color coding
Center column: Arrow pointing right labeled 'Solution', neutral gray
Right column: 'After' scenario with benefits listed, green color coding

Each column vertically aligned at top, creating balanced composition.
```

**Модульная сетка:**
```
Grid-based layout with 12-column structure:
- Header spans all 12 columns
- Content divided into 4 equal modules (3 columns each)
- Each module contains: icon (top), heading (middle), description (bottom)
- Consistent 24px gutter spacing between modules
- All modules aligned to invisible baseline grid
```

**Визуальный поток:**
```
Guide viewer's eye using visual hierarchy:
Start: Large number '89%' in top-left corner (entry point)
Flow: Curved arrow connecting to bar chart in center
Continue: Dotted line leading to conclusion box on right
End: Call-to-action button in bottom-right (exit point)
```

### 5. Стиль (Style) - Визуальный язык

**Три основных эстетики:**

**Flat Design (плоский дизайн) - Рекомендуется по умолчанию:**
```
Modern flat design aesthetic, no shadows or gradients on shapes,
solid color fills, simple geometric primitives (circles, rectangles),
2D appearance with visual hierarchy through color and size only,
clean vector-style crisp edges
```

**Corporate/Business (корпоративный):**
```
Professional business infographic style, conservative color palette
(navy blue, gray, white), traditional sans-serif typography,
data-focused with minimal decoration, trustworthy and authoritative aesthetic,
suitable for board presentation or annual report
```

**Educational/Playful (образовательный):**
```
Friendly approachable design, warm vibrant colors (orange, teal, yellow),
rounded shapes instead of sharp edges, illustrated icons with personality,
inviting and engaging for learning context, slightly playful but still professional
```

---

## Текст в Инфографике: Explicit Content Strategy

**Уникальная возможность Nano Banana Pro:** Модель может генерировать **связный читаемый текст**, в отличие от старых моделей. Используйте это!

### Принцип явного указания текста

**Всегда прописывайте ТОЧНЫЙ текст**, который должен появиться на инфографике, в кавычках:

```
Title text: 'THE FUTURE OF REMOTE WORK'
Subtitle: 'How COVID-19 permanently changed workplace dynamics'

Section 1 heading: 'Productivity Metrics'
Body text below: 'Teams working remotely reported 23% higher output compared
to traditional office environment, measured across 500 companies.'

Section 2 heading: 'Cost Savings'
Statistic: '$11,000' with label underneath: 'Average annual savings per employee'
```

### Типографическая иерархия

**Определите явные уровни:**

```
Typography hierarchy:
Level 1 (Main title): Bold sans-serif, 72pt equivalent, color #1E293B, all caps
Level 2 (Section headings): Bold sans-serif, 48pt equivalent, color #334155
Level 3 (Body text): Regular sans-serif, 24pt equivalent, color #64748B
Level 4 (Captions/sources): Light sans-serif, 18pt equivalent, color #94A3B8

All text high contrast against background, minimum 4.5:1 ratio for accessibility.
```

### Читаемость текста

**Критичные параметры:**

```
Text readability optimizations:
- Minimum font size 18pt equivalent (nothing smaller)
- Line length maximum 60-70 characters for body text
- Line height (leading) 1.5x font size for comfortable reading
- Letter spacing slightly increased (+2%) for all-caps headings
- No text on busy backgrounds - always use solid color or blur overlay
- High contrast: dark text (#1F2937) on light background (#FFFFFF) or vice versa
```

---

## Визуализация Данных: Типы и Специфика

### Bar Chart (Столбчатая диаграмма)

**Когда использовать:** Сравнение дискретных категорий

**Промпт-структура:**
```
Bar chart visualization showing quarterly sales comparison.
Chart structure:
- Horizontal x-axis labeled 'Quarter' with four categories: Q1, Q2, Q3, Q4
- Vertical y-axis labeled 'Revenue ($ Million)' with scale from 0 to 100
- Four vertical bars with exact heights:
  Q1: 45M (bar height 45% of y-axis max)
  Q2: 62M (bar height 62%)
  Q3: 58M (bar height 58%)
  Q4: 78M (bar height 78%)
- Bars filled with gradient blue (#3B82F6 to #1E40AF)
- Each bar labeled with exact value on top in white text
- Subtle horizontal grid lines every 20M for reference
- Q4 bar highlighted with gold outline indicating record quarter
```

### Pie Chart (Круговая диаграмма)

**Когда использовать:** Показать части целого (проценты до 100%)

**Промпт-структура:**
```
Pie chart showing market share distribution among 4 competitors.
Chart structure:
- Circular pie divided into 4 segments, clockwise from top:
  Segment 1 (Company A): 42% of circle, blue #2563EB, starting at 12 o'clock
  Segment 2 (Company B): 28% of circle, orange #F97316
  Segment 3 (Company C): 19% of circle, green #10B981
  Segment 4 (Company D): 11% of circle, gray #6B7280
- Each segment labeled INSIDE with percentage '42%' and company name 'Company A'
- White text on colored segments for contrast
- Slight separation (2px gap) between segments for clarity
- Legend box on right side listing all companies with color swatches
```

### Line Graph (Линейный график)

**Когда использовать:** Показать тренд во времени

**Промпт-структура:**
```
Line graph showing website traffic growth over 12 months.
Chart structure:
- Horizontal x-axis labeled 'Month' with 12 points: Jan through Dec
- Vertical y-axis labeled 'Visitors' with scale 0 to 100K
- Single smooth curved line connecting data points:
  Jan: 15K, Feb: 18K, Mar: 22K, Apr: 28K, May: 35K, Jun: 42K,
  Jul: 48K, Aug: 52K, Sep: 58K, Oct: 64K, Nov: 72K, Dec: 85K
- Line color: gradient from blue to purple
- Data points marked with small circles at each month
- Area under line filled with semi-transparent blue gradient
- Annotation arrow pointing to Jun-Jul period with note: 'Marketing campaign launch'
```

### Progress/Funnel (Воронка)

**Когда использовать:** Показать конверсию через этапы

**Промпт-структура:**
```
Conversion funnel diagram showing customer journey.
Funnel structure: Five horizontal bars stacked vertically, decreasing in width:
Stage 1 (top): 'Website Visitors' - 100,000 users - full width bar, light blue
Stage 2: 'Product Page Views' - 45,000 users - 45% width, medium blue
Stage 3: 'Add to Cart' - 18,000 users - 18% width, darker blue
Stage 4: 'Checkout Started' - 9,000 users - 9% width, navy blue
Stage 5 (bottom): 'Purchase Complete' - 3,500 users - 3.5% width, dark navy

Each bar labeled on left with stage name, on right with number and percentage.
Conversion rate between stages shown with small text: '45% →' between stages 1-2.
Bars centered vertically creating trapezoid funnel shape.
```

---

## Детальные Примеры по Категориям

### Пример 1: Статистическая Инфографика (Бизнес-метрики)

**Тип:** Dashboard-style одностраничный отчет

```
Professional business statistics infographic dashboard.

Subject: Q4 2025 Company Performance Overview showcasing four key metrics
for executive summary presentation.

Layout Structure:
Canvas: Horizontal landscape 16:9 format, optimized for PowerPoint/Keynote.

Header Section (top 20% of canvas):
- Title: 'Q4 2025 PERFORMANCE DASHBOARD' in bold sans-serif all caps,
  positioned top-center, color dark navy #1E293B, 64pt equivalent.
- Subtitle below: 'Year-over-year growth highlights' in lighter weight,
  color medium gray #64748B, 32pt equivalent.
- Company logo positioned top-right corner, 80px height.

Main Content Grid (middle 70% of canvas):
Divided into 2x2 grid with equal-sized quadrants, 32px gutter spacing:

Quadrant 1 (Top-Left): Revenue Metric
- Large number: '$4.2M' in bold, color success green #10B981, 96pt
- Label below: 'Total Revenue' in regular weight, 28pt
- Small trend indicator: upward arrow icon + '↑ 34%' in green
- Mini sparkline graph below showing 6-month trend

Quadrant 2 (Top-Right): Customer Growth
- Large number: '12,450' in bold, color blue #2563EB, 96pt
- Label: 'New Customers' in regular weight, 28pt
- Trend: upward arrow '↑ 23%'
- Icon: simplified user silhouette above number

Quadrant 3 (Bottom-Left): Retention Rate
- Circular progress ring showing 89% filled, color orange #F97316
- Center: '89%' in large bold text
- Label: 'Customer Retention' below ring
- Comparison text: 'Target: 85%' with checkmark

Quadrant 4 (Bottom-Right): Market Share
- Pie chart with 3 segments:
  Us: 42% (blue), Competitor A: 31% (gray), Others: 27% (light gray)
- Label: 'Market Position' above chart
- Key insight text: 'Industry leader' below

Footer Section (bottom 10%):
- Left: Data source 'Internal Analytics, Dec 2025' in small text
- Right: Call-to-action text 'Full report: company.com/q4'

Background: Clean white #FFFFFF with very subtle light gray grid pattern
for professional appearance.

Typography: Inter or similar modern sans-serif throughout, weights 400-700.

Color Palette: Primary navy #1E293B, accent colors for metrics (green, blue,
orange), neutrals gray #64748B and #94A3B8.

Style: Modern corporate dashboard aesthetic, flat design with no shadows,
crisp clean presentation suitable for executive briefing, data-driven and
professional, minimal decorative elements, focus on clarity and quick comprehension.

Negative Prompt: Cluttered layout, decorative illustrations, gradients on background,
3D effects, script fonts, low contrast text, busy patterns, cartoon icons.
```

### Пример 2: Процессная Инфографика (How-To Guide)

**Тип:** 5-шаговая инструкция

```
Step-by-step process infographic explaining content creation workflow.

Subject: 'How to Create Engaging Social Media Content in 5 Steps' - educational
guide for marketing beginners showing linear progression from ideation to publishing.

Data Story: Takes viewer through complete content creation process with clear
actionable steps, each building on previous, culminating in successful post.

Layout Structure:
Canvas: Vertical portrait 9:16 format for Instagram Stories / mobile viewing.

Header (top 12%):
- Title: 'CREATE ENGAGING CONTENT' centered, bold all-caps, color #1F2937, 48pt
- Subtitle: 'Your 5-step workflow' in lighter text, 24pt

Content Area (middle 76%):
Five numbered steps arranged vertically with connecting flow arrows:

Step 1 (20% width):
- Number '1' in large circle, diameter 80px, filled blue #3B82F6, white text
- Icon: lightbulb symbol below number, 64px, line art style
- Heading: 'BRAINSTORM IDEAS' in bold, 32pt
- Body text: 'Research trending topics in your niche. List 10 potential
  content angles. Focus on audience pain points.'
- Right-pointing arrow connecting to Step 2, color blue

Step 2:
- Number '2' in circle, filled deeper blue #2563EB
- Icon: pencil and paper
- Heading: 'WRITE YOUR COPY'
- Body text: 'Draft compelling caption with hook in first sentence.
  Keep it under 150 words. Include clear call-to-action.'
- Arrow to Step 3

Step 3:
- Number '3' in circle, filled purple #8B5CF6
- Icon: camera or image frame
- Heading: 'CREATE VISUALS'
- Body text: 'Design eye-catching graphics or select high-quality photos.
  Maintain brand color palette. Use text overlays for key points.'
- Arrow to Step 4

Step 4:
- Number '4' in circle, filled pink #EC4899
- Icon: calendar with checkmark
- Heading: 'SCHEDULE POST'
- Body text: 'Use analytics to find optimal posting time for your audience.
  Schedule 1-2 weeks in advance for consistency.'
- Arrow to Step 5

Step 5:
- Number '5' in circle, filled green #10B981
- Icon: graph trending upward
- Heading: 'ANALYZE RESULTS'
- Body text: 'Track engagement metrics: likes, comments, shares, saves.
  Identify what works. Refine strategy for next post.'

Footer (bottom 12%):
- Pro tip callout box with light blue background: 'Tip: Batch create content
  for entire week to save time and maintain consistency'

Background: White with very subtle confetti pattern in corners (light blue dots).

Typography: All sans-serif, headings Poppins Bold, body text Inter Regular.

Visual Flow: Numbers increase in size slightly as you progress (80px → 90px → 100px),
creating visual acceleration. Arrows vary in style (straight → curved → dotted)
to maintain visual interest while guiding eye down the page.

Color Strategy: Gradient progression from cool (blue) to warm (pink) to success
(green), subconsciously reinforcing journey from start to achievement.

Style: Educational and friendly, modern flat design, approachable for beginners,
visually engaging with clear hierarchy, optimized for mobile screenshot and sharing.

Negative Prompt: Corporate stiff aesthetic, all same color, tiny text, complex
jargon, abstract concepts, no clear numbers, confusing flow, overlapping elements.
```

### Пример 3: Сравнительная Инфографика (Product Comparison)

**Тип:** Side-by-side план-сравнение

```
Product pricing comparison infographic for SaaS subscription tiers.

Subject: Three-tier pricing structure (Basic, Pro, Enterprise) presented
in clean comparison format helping users choose appropriate plan.

Layout Structure:
Canvas: Horizontal landscape 16:9, designed for website landing page hero section.

Header (top 15%):
- Title: 'CHOOSE YOUR PLAN' centered, 72pt bold
- Subtitle: 'All plans include 14-day free trial' 24pt regular

Main Content (middle 75%):
Three equal-width vertical columns (30% each), 5% spacing between:

Column 1 - BASIC PLAN:
Background: White card with light gray border, subtle shadow
Header area: Light blue background #EFF6FF
- Plan name: 'Basic' in 48pt bold, centered
- Price: '$29/month' in 64pt bold, centered below name
- Tagline: 'For individuals' in 18pt italic

Features section (list format):
- Checkmark icon + 'Up to 5 projects'
- Checkmark icon + '10GB storage'
- Checkmark icon + 'Email support'
- Checkmark icon + 'Basic analytics'
- X icon (gray) + 'No custom branding'
- X icon + 'No API access'

Button: 'Start Free Trial' outlined blue button at bottom

Column 2 - PRO PLAN (HIGHLIGHTED):
Background: White card with THICK blue border #2563EB, elevated shadow (recommended)
Ribbon: 'MOST POPULAR' badge angled at top-right corner, orange background
Header area: Solid blue background #2563EB with white text
- Plan name: 'Pro' in 48pt bold white
- Price: '$79/month' in 64pt bold white
- Tagline: 'For growing teams' in 18pt white

Features section:
- Checkmark + 'Unlimited projects'
- Checkmark + '100GB storage'
- Checkmark + 'Priority support'
- Checkmark + 'Advanced analytics'
- Checkmark + 'Custom branding' (highlighted in green - new vs Basic)
- Checkmark + 'API access' (highlighted in green)

Button: 'Start Free Trial' FILLED blue button (primary CTA)

Column 3 - ENTERPRISE:
Background: White card with gray border, normal shadow
Header area: Dark gray background #1F2937 with white text
- Plan name: 'Enterprise' in 48pt bold white
- Price: 'Custom pricing' in 48pt (not as large) white
- Tagline: 'For large organizations' in 18pt white

Features section:
- Checkmark + 'Everything in Pro, plus:'
- Checkmark + 'Unlimited storage'
- Checkmark + 'Dedicated account manager'
- Checkmark + 'SLA guarantee'
- Checkmark + 'On-premise deployment'
- Checkmark + 'Custom integrations'

Button: 'Contact Sales' outlined gray button

Footer (bottom 10%):
- Centered text: 'All plans can be canceled anytime. No hidden fees.'
  Small print, gray color.
- Icons showing accepted payment methods (Visa, MC, AmEx)

Visual Hierarchy: Center column (Pro) is elevated 20px higher than side columns,
has thicker border, uses saturated blue to draw attention as recommended option.

Typography: Sans-serif throughout, pricing numbers in heavier weight (700) than
feature text (400) to emphasize cost anchoring.

Color Strategy:
- Basic: Cool colors, muted (less exciting but approachable)
- Pro: Vibrant blue (energetic, action-oriented) - hero
- Enterprise: Professional dark gray (serious, corporate)

Style: Clean modern SaaS pricing page aesthetic, flat design cards with minimal
shadows for depth, high legibility, designed for quick scanning and decision-making,
professional and trustworthy presentation.

Negative Prompt: Cluttered features list, inconsistent spacing, low contrast text,
missing prices, unclear differences between tiers, decorative illustrations that
distract from comparison, gradient backgrounds reducing readability.
```

### Пример 4: Timeline Инфографика (Хронология)

**Тип:** Историческая лента событий

```
Timeline infographic showing evolution of electric vehicles from 1832 to 2025.

Subject: Historical timeline documenting major milestones in electric vehicle
development, educational content for automotive enthusiasts showing technological
progression over 200 years.

Data Story: Demonstrates that EVs are not new invention but cyclical innovation -
early promise in 1800s, decline with gasoline engines, recent renaissance driven
by battery technology and climate concerns.

Layout Structure:
Canvas: Horizontal landscape ultra-wide 21:9 for scrolling web experience.

Design Pattern: Serpentine (S-curve) timeline flowing left-to-right, then back.

Timeline Visual Structure:
Central horizontal spine (line 8px thick, color #3B82F6) running full width
with alternating event nodes above and below line:

Milestone 1 (1832) - ABOVE LINE:
- Year marker: '1832' in large bold 48pt, positioned on timeline
- Circular node on spine, 60px diameter, filled blue
- Icon: Simple carriage illustration, line art style
- Event card above node:
  Background white, 300px width, rounded corners
  Heading: 'First Electric Carriage' bold 28pt
  Body text: 'Robert Anderson builds first crude electric vehicle
  in Scotland using non-rechargeable batteries.'
  Small historical photo or illustration if available

Milestone 2 (1891) - BELOW LINE:
- Year: '1891' on spine
- Node: 60px circle
- Icon: Battery symbol
- Event card below:
  Heading: 'Rechargeable Battery Invented'
  Body: 'William Morrison creates first successful electric car
  in USA with rechargeable battery, top speed 14 mph.'

Milestone 3 (1900) - ABOVE LINE:
- Year: '1900'
- Highlight: Different color (gold #F59E0B) indicating peak
- Event: 'Peak Market Share: EVs outsell gasoline cars in America,
  40% of all vehicles electric'
- Larger card emphasizing this was golden era

Milestone 4 (1908) - BELOW LINE:
- Year: '1908'
- Node: Red color indicating turning point
- Event: 'Model T Ford Launches - mass-produced gasoline cars
  become affordable, beginning of EV decline'

[Timeline continues through several more milestones...]

Milestone 8 (1997) - ABOVE LINE:
- Year: '1997'
- Node: Green color - renaissance begins
- Event: 'Toyota Prius - first mass-market hybrid vehicle
  reignites interest in electric propulsion'

Milestone 9 (2012) - BELOW LINE:
- Event: 'Tesla Model S launched, proving EVs can be desirable
  luxury vehicles. 265-mile range.'

Milestone 10 (2025) - ABOVE LINE:
- Year: '2025' - PRESENT DAY indicator
- Node: Animated pulse effect (if static, use concentric circles)
- Event: 'EVs reach 25% of global new car sales. 100+ models
  available. Average range 350 miles.'

Header (top of canvas):
- Title: 'THE RISE, FALL & REBIRTH OF ELECTRIC VEHICLES' in display font, 96pt
- Subtitle: 'Two centuries of innovation and setbacks' 36pt

Legend (bottom-left corner):
- Color coding key:
  Blue nodes: Technological breakthrough
  Gold nodes: Market milestone
  Red nodes: Setback/decline
  Green nodes: Revival era

Footer (bottom-right):
- Sources: 'Data compiled from IEEE, SAE International, automotive historians'

Background: Light beige parchment texture (#FEF3C7) giving historical document feel,
subtle and doesn't interfere with readability.

Typography:
- Years: Bold condensed sans-serif for compact timeline markers
- Headings: Display serif font for historical gravitas
- Body text: Modern sans-serif for readability

Visual Flow: Eye enters at left 1832, follows serpentine path through events,
alternating focus above/below keeps engagement, arrives at present day on right
showing clear progression. Varying node sizes (larger for more significant events)
creates rhythm.

Style: Historical infographic meets modern data visualization, blend of vintage
aesthetic (sepia tones, archival photo treatment) with clean contemporary
information design, educational museum exhibit quality.

Negative Prompt: Confusing timeline direction, events overlapping, illegible years,
inconsistent card sizes, too much text per event, cluttered with decorations,
no clear visual hierarchy between major/minor milestones.
```

---

## Негативные промпты для устранения проблем

**Универсальный негативный промпт для инфографики:**
```
Cluttered layout, too much text, illegible small fonts, low contrast text,
decorative elements that don't serve purpose, inconsistent icon styles,
misaligned elements, random spacing, too many colors, gradients on text,
3D effects reducing readability, busy background patterns, comic sans font,
arbitrary data visualization, unlabeled axes, missing units on numbers,
unclear hierarchy, no white space, cramped composition
```

**Для бизнес-инфографики:**
```
Unprofessional fonts, cartoon aesthetics, overly playful colors,
inaccurate data representation, missing sources, vague statistics,
unclear conclusions
```

**Для образовательной инфографики:**
```
Academic jargon without explanation, complex terminology, tiny footnotes,
inaccessible design, not beginner-friendly, assumes prior knowledge
```

**Для презентационных слайдов:**
```
Text-heavy slides, bullet point overload, no visual anchors,
inconsistent branding, poor projection readability, complex animations
in static design
```

---

## Чеклист перед генерацией

✅ **Субъект/Данные:**
- [ ] Точно определена тема и ключевое сообщение
- [ ] Данные конкретные (числа, проценты, категории)
- [ ] Понятно, что должен вынести зритель

✅ **Текстовое содержание:**
- [ ] Написан точный текст для заголовка
- [ ] Прописаны все лейблы и подписи
- [ ] Указаны числовые значения где применимо
- [ ] Определена иерархия (H1, H2, body text)

✅ **Структура макета:**
- [ ] Выбран формат (портрет/ландшафт/квадрат)
- [ ] Определены основные зоны (header/content/footer)
- [ ] Описана организация элементов (grid/vertical/columns)
- [ ] Указан визуальный поток (откуда начинается взгляд → куда идет)

✅ **Визуализация данных:**
- [ ] Выбран подходящий тип графика (bar/pie/line)
- [ ] Указаны оси и шкалы
- [ ] Прописаны точные значения данных
- [ ] Определена цветовая кодировка

✅ **Стиль:**
- [ ] Выбрана эстетика (flat/corporate/educational)
- [ ] Определена цветовая палитра (2-4 цвета)
- [ ] Указан стиль иконок (line art/flat/isometric)
- [ ] Типографика (шрифты и веса)

✅ **Негативный промпт:**
- [ ] Добавлены ограничения для предотвращения проблем

---

## Типичные ошибки и решения

| Проблема | Причина | Решение |
|----------|---------|---------|
| Нечитаемый текст | Недостаточная спецификация размеров | Указать явно: "minimum 18pt font size, high contrast #1F2937 on #FFFFFF" |
| Нелогичное расположение элементов | Не описана структура | Использовать секционирование: "divide into header/content/footer", "3-column grid" |
| Несвязная информация | Отсутствие нарратива | Описать "Data Story": "shows progression from problem to solution" |
| Текст не на том языке | Не прописан точный текст | Писать в кавычках: Title: 'YOUR EXACT TEXT HERE' |
| Перегруженная композиция | Слишком много элементов | Минимализм: "maximum 3 key metrics, generous white space, focus on clarity" |
| Несогласованные цвета | Цвета не определены явно | Задать палитру: "color palette limited to blue #2563EB, orange #F97316, gray #64748B" |

---

**Версия:** 2.0 (Методология "Structure-First" + Layout Logic)
**Обновлено:** 2026-01-06
**Базируется на:** Технический отчет "Архитектура промпт-инжиниринга Nano Banana Pro"
