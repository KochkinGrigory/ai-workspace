# Brand Assets - Централизованное хранилище брендов

> **Важно:** Начиная с версии 1.5.0, все брендовые ресурсы находятся в `/opt/ai-workspace/assets/brands/` и доступны через симлинк `brands/` → `/opt/ai-workspace/assets/brands/`

**Локация:** `brands/` (симлинк на `/opt/ai-workspace/assets/brands/`)

**Назначение:** Единое хранилище для всех брендов с guidelines + assets, доступное всем skills (nano-banana, website-pages, dashboard-pages, pdf).

## Структура хранилища

```
brands/
├── README.md                    # Документация хранилища
├── _templates/                  # Шаблоны для новых брендов
│   ├── colors.txt.example
│   ├── typography.txt.example
│   └── visual_style.md.example
├── фонд/
│   ├── README.md               # О бренде
│   ├── guidelines/             # Текстовые описания стиля
│   │   ├── colors.txt
│   │   ├── typography.txt
│   │   └── visual_style.md
│   └── assets/                 # Визуальные ресурсы
│       ├── logos/
│       ├── characters/
│       ├── products/
│       ├── templates/
│       └── backgrounds/
├── люкс-оптика/
├── ангелы-зрения/
└── оптика-будущего/
```

## Brand Guidelines - Руководство по фирменному стилю

**Локация:** `brands/[бренд]/guidelines/`

**Назначение:** Текстовые описания фирменного стиля, которые Claude автоматически читает перед генерацией.

### Как работает

```
Пользователь: "Создай презентацию для Фонда"

Claude:
1. Определяет бренд: "Фонд" → brands/фонд/
2. Читает: brands/фонд/guidelines/colors.txt → извлекает палитру
3. Читает: brands/фонд/guidelines/typography.txt → узнает шрифты
4. Читает: brands/фонд/guidelines/visual_style.md → понимает стиль
5. Находит: brands/фонд/assets/logos/ → логотипы
6. Формирует промпт с учетом всех гайдлайнов:
   "Professional presentation for Fond,
    colors: primary blue #0066CC, secondary orange #FF6600,
    Inter font family bold headings,
    minimalist modern style, 8px rounded corners,
    clean geometric shapes, lots of white space,
    modular grid layout, subtle shadows"
7. Генерирует изображение с использованием логотипа как референса
```

### Формат файлов

- **`.txt`** - структурированный текст (цвета, шрифты)
- **`.md`** - Markdown для описаний (стиль, tone of voice)
- **`.pdf`** - полные брендбуки (Claude может читать)

**Шаблоны:** `brands/_templates/*.example` - шаблоны для создания guidelines новых брендов

---

## Brand Assets - Визуальные ресурсы бренда

**Локация:** `brands/[бренд]/assets/`

**Назначение:** Визуальные референсы для применения через `--reference-images` (логотипы, персонажи, продукты, шаблоны, фоны).

### Структура assets

```
brands/[бренд]/assets/
├── logos/              # Логотипы бренда (PNG с прозрачностью)
├── characters/         # Фирменные персонажи и маскоты
├── products/           # Изображения продуктов
├── templates/          # Шаблоны макетов
└── backgrounds/        # Фоны и текстуры
```

### Категории assets

#### logos/
Логотипы бренда для встраивания в изображения
- PNG с прозрачным фоном (обязательно)
- Высокое разрешение (минимум 1000px)
- Несколько вариантов (default, horizontal, white, dark)

#### characters/
Фирменные персонажи и маскоты
- Для консистентного использования в разных сценах
- Несколько ракурсов (фронт, профиль, 3/4)
- Разные эмоции/выражения

#### products/
Изображения продуктов для стилизации
- `product_a_front.jpg` - фронтальный вид
- `product_a_angle.jpg` - ракурс 3/4
- `product_style_reference.jpg` - референс стиля съемки

#### templates/
Шаблоны макетов и композиций
- `presentation_title.png` - шаблон титульного слайда
- `presentation_content.png` - шаблон контентного слайда
- `social_post_template.png` - шаблон для соцсетей
- `infographic_layout.png` - композиция инфографики

#### backgrounds/
Фоны и текстуры для композитинга
- `studio_white.jpg` - студийный белый фон
- `studio_gradient.jpg` - градиентный фон
- `texture_concrete.jpg` - бетонная текстура
- `abstract_shapes.png` - абстрактные элементы

## Как Claude использует хранилище

**Автоматическое определение бренда и ресурсов:**

Claude анализирует запрос пользователя и автоматически:
1. **Определяет бренд** из запроса (Фонд, Люкс Оптика, Ангелы Зрения, etc.)
2. **Читает guidelines/** для извлечения стиля
3. **Ищет assets/** для референсных изображений
4. **Применяет всё вместе** при генерации
5. **Формирует оптимальный промпт** с учетом guidelines + assets

### Примеры использования

**Пример 1: Маскот бренда**
```
Пользователь: "Создай изображение маскота Ангелы Зрения в офисе"

Claude:
1. Определяет бренд: "Ангелы Зрения" → brands/ангелы-зрения/
2. Ищет персонажа: ls brands/ангелы-зрения/assets/characters/
3. Находит: angels_boy_mascote_default.png
4. Читает guidelines (если заполнены): colors.txt, visual_style.md
5. Генерирует с референсом:
   python3 generate.py "Angels Vision mascot boy in modern office" \
     --reference-images brands/ангелы-зрения/assets/characters/angels_boy_mascote_default.png
```

**Пример 2: Презентация с брендингом**
```
Пользователь: "Сделай презентационный слайд для Фонда"

Claude:
1. Определяет бренд: "Фонд" → brands/фонд/
2. Читает: brands/фонд/guidelines/colors.txt, typography.txt, visual_style.md
3. Находит логотипы: brands/фонд/assets/logos/fond_logo_default.png
4. Формирует промпт с фирменным стилем + использует логотип как референс
5. Генерирует презентацию
```

## Добавление новых брендов и ресурсов

### Создание нового бренда

```bash
# 1. Создать структуру
cd /opt/ai-workspace/assets/brands/
mkdir -p "новый-бренд"/{guidelines,assets/{logos,characters,products,templates,backgrounds}}

# 2. Скопировать шаблоны guidelines
cp _templates/*.example "новый-бренд/guidelines/"

# 3. Заполнить guidelines (переименовать .example и отредактировать)
cd "новый-бренд/guidelines/"
mv colors.txt.example colors.txt
# Отредактировать colors.txt с реальными данными бренда

# 4. Добавить assets (логотипы, персонажей)
cp /path/to/logo.png "новый-бренд/assets/logos/"

# 5. Создать README.md для бренда
# 6. Claude автоматически обнаружит и начнет использовать
```

### Добавление ресурсов в существующий бренд

```bash
# Добавить логотип
cp /path/to/logo_white.png /opt/ai-workspace/assets/brands/фонд/assets/logos/

# Добавить персонажа
cp /path/to/character.png /opt/ai-workspace/assets/brands/ангелы-зрения/assets/characters/

# Claude автоматически обнаружит новые файлы
```

### Рекомендуемые форматы

- **Логотипы:** PNG с прозрачностью, минимум 1000px
- **Персонажи:** PNG/JPG, несколько ракурсов, 2048px+
- **Продукты:** JPG высокого качества, хорошее освещение
- **Шаблоны:** PNG/JPG, примеры композиции

## Текущие бренды

| Бренд | Логотипы | Персонажи | Guidelines | Локация |
|-------|----------|-----------|------------|---------|
| **Фонд** | 2 варианта | - | Пусто | `brands/фонд/` |
| **Люкс Оптика** | 1 вариант | - | Пусто | `brands/люкс-оптика/` |
| **Ангелы Зрения** | 2 варианта | 1 маскот (30MB) | Пусто | `brands/ангелы-зрения/` |
| **Оптика Будущего** | 1 вариант | - | Пусто | `brands/оптика-будущего/` |

**Примеры использования:**
- "Добавь логотип Фонда" → `brands/фонд/assets/logos/fond_logo_default.png`
- "Маскот Ангелы Зрения в офисе" → `brands/ангелы-зрения/assets/characters/angels_boy_mascote_default.png`
- "Логотип Люкс Оптика" → `brands/люкс-оптика/assets/logos/lux_optics_logo.png`
