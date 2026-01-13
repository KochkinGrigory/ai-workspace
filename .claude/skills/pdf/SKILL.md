---
name: pdf
description: |
  Работа с PDF файлами: извлечение текста/таблиц, создание, объединение/разделение, заполнение форм, OCR. ИСПОЛЬЗУЙ ЭТОТ SKILL КОГДА: пользователь просит (1) Извлечь текст или таблицы из PDF, (2) Создать новый PDF с нуля (отчеты, документы), (3) Объединить/разделить PDF файлы, (4) Заполнить PDF форму программно, (5) Добавить водяной знак или шифрование, (6) OCR для сканированных PDF (распознавание текста), (7) Извлечь изображения из PDF, (8) Конвертировать PDF в изображения. Автоматически использует pypdf для базовых операций, pdfplumber для извлечения таблиц, reportlab для создания PDF (с шрифтом Manrope для кириллицы), pytesseract для OCR сканированных документов.
allowed-tools: Read, Write, Edit, Bash(cmd:*), Bash(python:*), Bash(python3:*)
version: 1.1.0
author: PDF Processing Team
license: Proprietary. LICENSE.txt has complete terms
---

# PDF Processing Guide

## Overview

This guide covers essential PDF processing operations using Python libraries and command-line tools.

**Когда использовать этот skill:**
- Извлечение данных из PDF (текст, таблицы, изображения)
- Создание PDF отчетов и документов
- Массовая обработка PDF файлов
- OCR для сканированных документов
- Программное заполнение PDF форм

## Quick Start

```python
from pypdf import PdfReader, PdfWriter

# Read a PDF
reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# Extract text
text = ""
for page in reader.pages:
    text += page.extract_text()
```

## Python Libraries

### pypdf - Basic Operations

#### Merge PDFs
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

#### Split PDF
```python
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

#### Extract Metadata
```python
reader = PdfReader("document.pdf")
meta = reader.metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Subject: {meta.subject}")
print(f"Creator: {meta.creator}")
```

#### Rotate Pages
```python
reader = PdfReader("input.pdf")
writer = PdfWriter()

page = reader.pages[0]
page.rotate(90)  # Rotate 90 degrees clockwise
writer.add_page(page)

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

### pdfplumber - Text and Table Extraction

#### Extract Text with Layout
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

#### Extract Tables
```python
with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"Table {j+1} on page {i+1}:")
            for row in table:
                print(row)
```

#### Advanced Table Extraction
```python
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:  # Check if table is not empty
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

# Combine all tables
if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("extracted_tables.xlsx", index=False)
```

### reportlab - Create PDFs

#### Basic PDF Creation
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter

# Add text
c.drawString(100, height - 100, "Hello World!")
c.drawString(100, height - 120, "This is a PDF created with reportlab")

# Add a line
c.line(100, height - 140, 400, height - 140)

# Save
c.save()
```

#### Create PDF with Multiple Pages
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Add content
title = Paragraph("Report Title", styles['Title'])
story.append(title)
story.append(Spacer(1, 12))

body = Paragraph("This is the body of the report. " * 20, styles['Normal'])
story.append(body)
story.append(PageBreak())

# Page 2
story.append(Paragraph("Page 2", styles['Heading1']))
story.append(Paragraph("Content for page 2", styles['Normal']))

# Build PDF
doc.build(story)
```

#### Unicode and Cyrillic Support

**ВАЖНО:** По умолчанию reportlab использует стандартные шрифты, которые НЕ поддерживают кириллицу. Для работы с русским текстом необходимо зарегистрировать Unicode-шрифт.

**Рекомендуемый шрифт:** Manrope (современный, профессиональный, поддержка Unicode)

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import A4

# 1. Зарегистрировать шрифт Manrope
pdfmetrics.registerFont(TTFont('Manrope', '/usr/share/fonts/truetype/manrope/Manrope.ttf'))

# 2. Создать стили с Manrope
doc = SimpleDocTemplate("report_russian.pdf", pagesize=A4)
story = []

custom_style = ParagraphStyle(
    'CustomStyle',
    fontName='Manrope',  # Используем Manrope
    fontSize=12
)

# 3. Создать контент с кириллицей
title = Paragraph("Аналитический отчет по продажам", custom_style)
story.append(title)

# 4. Сохранить
doc.build(story)
```

**Альтернативные шрифты с кириллицей:**
- **DejaVu Sans** - `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf`
- **Liberation Sans** - `/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf`

**Для таблиц:**
```python
from reportlab.platypus import Table, TableStyle

data = [
    ['Показатель', 'Значение'],
    ['Выручка', '3 500 000 ₽'],
    ['Клиентов', '842']
]

table = Table(data)
table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Manrope'),  # Указываем шрифт для всей таблицы
    ('FONTSIZE', (0, 0), (-1, -1), 11),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))
```

**Для matplotlib графиков:**
```python
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Добавить Manrope в matplotlib
manrope_path = '/usr/share/fonts/truetype/manrope/Manrope.ttf'
fm.fontManager.addfont(manrope_path)
plt.rcParams['font.family'] = 'Manrope'

# Теперь графики будут использовать Manrope
plt.plot([1, 2, 3], [1, 4, 9])
plt.xlabel('Недели')
plt.ylabel('Выручка (₽)')
plt.title('Динамика продаж')
```

## Command-Line Tools

### pdftotext (poppler-utils)
```bash
# Extract text
pdftotext input.pdf output.txt

# Extract text preserving layout
pdftotext -layout input.pdf output.txt

# Extract specific pages
pdftotext -f 1 -l 5 input.pdf output.txt  # Pages 1-5
```

### qpdf
```bash
# Merge PDFs
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# Split pages
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
qpdf input.pdf --pages . 6-10 -- pages6-10.pdf

# Rotate pages
qpdf input.pdf output.pdf --rotate=+90:1  # Rotate page 1 by 90 degrees

# Remove password
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf
```

### pdftk (if available)
```bash
# Merge
pdftk file1.pdf file2.pdf cat output merged.pdf

# Split
pdftk input.pdf burst

# Rotate
pdftk input.pdf rotate 1east output rotated.pdf
```

## Common Tasks

### Extract Text from Scanned PDFs
```python
# Requires: pip install pytesseract pdf2image
import pytesseract
from pdf2image import convert_from_path

# Convert PDF to images
images = convert_from_path('scanned.pdf')

# OCR each page
text = ""
for i, image in enumerate(images):
    text += f"Page {i+1}:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"

print(text)
```

### Add Watermark
```python
from pypdf import PdfReader, PdfWriter

# Create watermark (or load existing)
watermark = PdfReader("watermark.pdf").pages[0]

# Apply to all pages
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

### Extract Images
```bash
# Using pdfimages (poppler-utils)
pdfimages -j input.pdf output_prefix

# This extracts all images as output_prefix-000.jpg, output_prefix-001.jpg, etc.
```

### Password Protection
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

# Add password
writer.encrypt("userpassword", "ownerpassword")

with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```

## Quick Reference

| Task | Best Tool | Command/Code |
|------|-----------|--------------|
| Merge PDFs | pypdf | `writer.add_page(page)` |
| Split PDFs | pypdf | One page per file |
| Extract text | pdfplumber | `page.extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` |
| Create PDFs | reportlab | Canvas or Platypus |
| Command line merge | qpdf | `qpdf --empty --pages ...` |
| OCR scanned PDFs | pytesseract | Convert to image first |
| Fill PDF forms | pdf-lib or pypdf | См. [forms.md](references/forms.md) |

## Next Steps

- **Заполнение PDF форм:** см. [forms.md](references/forms.md) - пошаговое руководство с примерами
- **Продвинутые возможности:** см. [advanced-usage.md](references/advanced-usage.md) - pypdfium2, JavaScript библиотеки (pdf-lib)
- **Практические примеры:** см. [example-usage.md](examples/example-usage.md) - реальные кейсы использования
- **Troubleshooting:** см. [advanced-usage.md](references/advanced-usage.md) - решение типичных проблем

## Структура skill

```
pdf/
├── SKILL.md                    # Этот файл - основное руководство
├── LICENSE.txt                 # Лицензия
├── references/
│   ├── forms.md               # Работа с PDF формами
│   └── advanced-usage.md      # Продвинутые возможности и troubleshooting
├── examples/
│   └── example-usage.md       # Практические примеры использования
└── scripts/
    ├── fill_pdf_form_with_annotations.py
    ├── extract_form_field_info.py
    └── ... (вспомогательные скрипты)
```
