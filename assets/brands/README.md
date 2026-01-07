# Brands - Централизованное хранилище брендов

> Единое хранилище для всех брендовых ресурсов (guidelines + assets), доступное всем skills через симлинки

## Структура

```
brands/
├── README.md                    # Эта инструкция
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

## Назначение

Централизованное хранилище для:

1. **Brand Guidelines** - Текстовые описания фирменного стиля (цвета, шрифты, визуальный стиль)
2. **Brand Assets** - Визуальные ресурсы (логотипы, персонажи, продукты, шаблоны, фоны)

## Использование

### Доступ из skills

Все skills получают доступ к брендам через **символические ссылки**:

```bash
/opt/ai-workspace/.claude/skills/nano-banana-image-gen/brands → /opt/ai-workspace/assets/brands/
/opt/ai-workspace/.claude/skills/website-pages-generator/brands → /opt/ai-workspace/assets/brands/
/opt/ai-workspace/.claude/skills/dashboard-pages-generator/brands → /opt/ai-workspace/assets/brands/
/opt/ai-workspace/.claude/skills/pdf/brands → /opt/ai-workspace/assets/brands/
```

### Автоматическое применение

Claude автоматически:
1. **Определяет бренд** из запроса пользователя
2. **Читает guidelines/** для извлечения стиля
3. **Находит assets/** для использования в генерации
4. **Применяет всё вместе** при создании контента

**Примеры:**

```
Пользователь: "Создай презентацию для Фонда"

Claude:
1. Определяет: brands/фонд/
2. Читает: brands/фонд/guidelines/colors.txt → палитра
3. Читает: brands/фонд/guidelines/visual_style.md → стиль
4. Находит: brands/фонд/assets/logos/ → логотипы
5. Генерирует презентацию с учетом всех правил
```

```
Пользователь: "Логотип Ангелы Зрения на белом фоне"

Claude:
1. Определяет: brands/ангелы-зрения/
2. Находит: brands/ангелы-зрения/assets/logos/angels_vision_logo_with_descriptor.png
3. Использует логотип в генерации
```

## Структура бренда

Каждый бренд имеет:

### guidelines/ - Текстовые описания стиля

**colors.txt** - Цветовая палитра (HEX, RGB, названия)
```txt
# Фирменная цветовая палитра

## Primary Colors

Primary Blue
HEX: #0066CC
RGB: 0, 102, 204
Usage: Заголовки, кнопки, акценты
```

**typography.txt** - Правила шрифтов
```txt
# Типографика

## Primary Font
Font Family: Inter
Usage: Заголовки, UI элементы
Weights: Regular (400), Semibold (600), Bold (700)
```

**visual_style.md** - Визуальный стиль
```markdown
# Визуальный стиль

## Общая эстетика
Design Style: Minimalist Modern
Mood: Clean, Professional, Trustworthy

## Core Design Principles
### 1. Simplicity
- Minimum elements on screen
- Clear visual hierarchy
```

### assets/ - Визуальные ресурсы

**logos/** - Логотипы бренда
- PNG с прозрачным фоном
- Несколько вариантов (default, horizontal, white, dark)
- Высокое разрешение (минимум 1000px)

**characters/** - Фирменные персонажи и маскоты
- Для консистентного использования в разных сценах
- Несколько ракурсов (фронт, профиль, 3/4)
- Разные эмоции/выражения

**products/** - Изображения продуктов
- Для стилизации и референсов
- Профессиональная съемка
- Несколько ракурсов

**templates/** - Шаблоны макетов
- Композиционные схемы
- Макеты слайдов презентаций
- Шаблоны для соцсетей

**backgrounds/** - Фоны и текстуры
- Студийные фоны
- Текстуры (дерево, ткань, бетон)
- Фирменные фоны с брендингом

## Добавление нового бренда

### 1. Создать структуру

```bash
cd /opt/ai-workspace/assets/brands/
mkdir -p "новый-бренд"/{guidelines,assets/{logos,characters,products,templates,backgrounds}}
```

### 2. Заполнить guidelines

```bash
# Скопировать шаблоны
cp _templates/*.example "новый-бренд/guidelines/"

# Переименовать и заполнить
cd "новый-бренд/guidelines/"
mv colors.txt.example colors.txt
# Отредактировать colors.txt с реальными данными бренда
```

### 3. Добавить assets

```bash
# Добавить логотипы
cp /path/to/logo.png "новый-бренд/assets/logos/"

# Добавить персонажей (если есть)
cp /path/to/character.png "новый-бренд/assets/characters/"
```

### 4. Создать README

```bash
# Создать README.md для бренда
nano "новый-бренд/README.md"
```

Содержание README:
```markdown
# [Название бренда]

**Тип:** [Клиника / Партнер / Дочерняя компания]
**Создан:** 2026-01-XX
**Статус:** [Активен / Архив]

## Описание

[Краткое описание бренда]

## Assets

- **Логотипы:** [количество] вариантов
- **Персонажи:** [есть/нет]
- **Продукты:** [есть/нет]

## Guidelines

- [x] Цвета (colors.txt)
- [x] Типографика (typography.txt)
- [x] Визуальный стиль (visual_style.md)
```

## Текущие бренды

| Бренд | Логотипы | Персонажи | Guidelines | Статус |
|-------|----------|-----------|------------|--------|
| **Фонд** | 2 варианта | - | Пустые | ✅ Активен |
| **Люкс Оптика** | 1 вариант | - | Пустые | ✅ Активен |
| **Ангелы Зрения** | 2 варианта | 1 маскот | Пустые | ✅ Активен |
| **Оптика Будущего** | 1 вариант | - | Пустые | ✅ Активен |

## Best Practices

### Организация файлов

✅ **Понятные имена:** `brand_logo_primary.png`, `mascot_front_happy.png`
✅ **Версионирование:** `colors_v1.txt`, `colors_v2.txt`
✅ **Группировка:** Связанные файлы в одной папке
✅ **Документация:** README.md для каждого бренда

### Качество файлов

✅ **Логотипы:** PNG с прозрачностью, минимум 1000px
✅ **Персонажи:** Высокое разрешение, четкие детали
✅ **Продукты:** Профессиональная съемка, хорошее освещение
✅ **Фоны:** Минимум 2048px для универсальности

### Guidelines

✅ **Полнота:** Заполнить все 3 файла (colors, typography, visual_style)
✅ **Специфичность:** Конкретные значения (HEX, шрифты, размеры)
✅ **Актуальность:** Обновлять при ребрендинге
✅ **Консистентность:** Стиль должен соответствовать assets

## Интеграция со skills

### nano-banana-image-gen

```bash
# Автоматически использует:
brands/[бренд]/guidelines/ → для формирования промпта
brands/[бренд]/assets/logos/ → через --reference-images
brands/[бренд]/assets/characters/ → для консистентности персонажей
```

### website-pages-generator

```bash
# Автоматически использует:
brands/[бренд]/guidelines/colors.txt → для Tailwind CSS палитры
brands/[бренд]/guidelines/typography.txt → для шрифтов
brands/[бренд]/assets/logos/ → для встраивания в сайт
```

### dashboard-pages-generator

```bash
# Автоматически использует:
brands/[бренд]/guidelines/colors.txt → для ChartConfig палитры
brands/[бренд]/assets/logos/ → для header/footer
```

### pdf

```bash
# Автоматически использует:
brands/[бренд]/guidelines/ → для стилизации документов
brands/[бренд]/assets/logos/ → для встраивания в PDF
```

## Технические детали

### Поддерживаемые форматы

**Изображения:**
- PNG (рекомендуется для логотипов с прозрачностью)
- JPG (для фото продуктов и фонов)
- WEBP (альтернатива JPG)

**Текстовые файлы:**
- TXT (простые списки)
- MD (форматированные описания)
- PDF (полные брендбуки - можно хранить в guidelines/)

### Ограничения

- **Размер файла:** До 20MB на изображение
- **Разрешение:** Рекомендуется 1024px-4096px
- **Референсы:** До 14 изображений одновременно (для nano-banana)

### Симлинки

Симлинки создаются автоматически при настройке skill:

```bash
ln -s /opt/ai-workspace/assets/brands /opt/ai-workspace/.claude/skills/[skill-name]/brands
```

Проверка работы симлинка:

```bash
ls -la /opt/ai-workspace/.claude/skills/nano-banana-image-gen/brands
# Должно показать: brands -> /opt/ai-workspace/assets/brands/
```

## Преимущества централизации

✅ **Единый источник истины** - все skills используют одни и те же ресурсы
✅ **Переиспользование** - логотипы доступны везде (nano-banana, website, dashboard, pdf)
✅ **Масштабируемость** - легко добавить 10-20 брендов
✅ **Организация** - все ресурсы бренда (guidelines + assets) в одной папке
✅ **Версионирование** - легко коммитить изменения по брендам
✅ **DRY principle** - не дублируем файлы в каждом skill

---

**Версия:** 1.0
**Создано:** 2026-01-06
**Обновлено:** 2026-01-06
