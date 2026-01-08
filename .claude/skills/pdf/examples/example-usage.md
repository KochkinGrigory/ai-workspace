# Примеры использования PDF Skill

Реальные примеры работы со skill.

---

## Пример 1: Извлечение таблиц из накладной

### Команда пользователя:
```
Извлеки все таблицы из накладной invoice.pdf и сохрани в Excel
```

### Workflow:

**Шаг 1 - Анализ PDF:**
```python
import pdfplumber

with pdfplumber.open('invoice.pdf') as pdf:
    print(f"Страниц в документе: {len(pdf.pages)}")

    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        print(f"Страница {i+1}: найдено таблиц - {len(tables)}")
```

**Шаг 2 - Извлечение и экспорт:**
```python
import pandas as pd

all_tables = []
with pdfplumber.open('invoice.pdf') as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

# Объединяем и сохраняем
if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("invoice_tables.xlsx", index=False)
    print("✅ Таблицы извлечены в invoice_tables.xlsx")
```

**Результат:**
```
✅ Найдено таблиц: 3
✅ Создан файл: invoice_tables.xlsx
📊 Строк данных: 45
```

---

## Пример 2: Объединение нескольких договоров

### Команда:
```
Объедини все PDF файлы из папки contracts/ в один документ
```

### Workflow:

**Шаг 1 - Поиск файлов:**
```bash
ls contracts/*.pdf
# contracts/contract_001.pdf
# contracts/contract_002.pdf
# contracts/contract_003.pdf
```

**Шаг 2 - Объединение:**
```python
from pypdf import PdfWriter, PdfReader
import os
from pathlib import Path

writer = PdfWriter()
contracts_dir = Path("contracts")

# Сортируем файлы по имени
pdf_files = sorted(contracts_dir.glob("*.pdf"))

for pdf_file in pdf_files:
    print(f"Добавляем: {pdf_file.name}")
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

# Сохраняем объединенный файл
with open("all_contracts_merged.pdf", "wb") as output:
    writer.write(output)

print(f"✅ Объединено файлов: {len(pdf_files)}")
print(f"✅ Всего страниц: {len(writer.pages)}")
```

**Результат:**
```
✅ Объединено файлов: 3
✅ Всего страниц: 24
📁 Создан файл: all_contracts_merged.pdf
```

---

## Пример 3: Извлечение текста из сканированного документа (OCR)

### Команда:
```
Извлеки текст из отсканированного паспорта scan.pdf
```

### Workflow:

**Шаг 1 - Проверка на сканирование:**
```python
from pypdf import PdfReader

reader = PdfReader("scan.pdf")
text = reader.pages[0].extract_text()

if not text.strip():
    print("⚠️ Документ отсканирован, нужен OCR")
else:
    print("✅ Документ содержит текстовый слой")
```

**Шаг 2 - OCR с Tesseract:**
```python
import pytesseract
from pdf2image import convert_from_path

# Конвертируем PDF в изображения
images = convert_from_path('scan.pdf', dpi=300)

# OCR для каждой страницы
full_text = ""
for i, image in enumerate(images):
    print(f"Обрабатываю страницу {i+1}...")
    page_text = pytesseract.image_to_string(image, lang='rus')
    full_text += f"=== Страница {i+1} ===\n{page_text}\n\n"

# Сохраняем
with open("extracted_text.txt", "w", encoding="utf-8") as f:
    f.write(full_text)

print("✅ Текст извлечен и сохранен")
```

**Результат:**
```
✅ Обработано страниц: 2
✅ Распознано символов: ~1500
📄 Создан файл: extracted_text.txt
```

---

## Пример 4: Создание отчета в PDF

### Команда:
```
Создай PDF отчет по продажам за декабрь с таблицей и графиком
```

### Workflow:

**Шаг 1 - Подготовка данных:**
```python
import pandas as pd

# Данные продаж
sales_data = {
    'Дата': ['01.12', '08.12', '15.12', '22.12', '29.12'],
    'Продажи': [150000, 180000, 220000, 195000, 240000]
}
df = pd.DataFrame(sales_data)
```

**Шаг 2 - Создание PDF:**
```python
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch

doc = SimpleDocTemplate("sales_report_december.pdf", pagesize=A4)
styles = getSampleStyleSheet()
story = []

# Заголовок
title = Paragraph("Отчет по продажам - Декабрь 2025", styles['Title'])
story.append(title)
story.append(Spacer(1, 0.5*inch))

# Таблица
table_data = [['Дата', 'Продажи (₽)']]
table_data.extend(df.values.tolist())

table = Table(table_data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 14),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))

story.append(table)
story.append(Spacer(1, 0.5*inch))

# Итоги
total = df['Продажи'].sum()
summary = Paragraph(f"<b>Итого за месяц:</b> {total:,} ₽", styles['Heading2'])
story.append(summary)

# Генерация PDF
doc.build(story)
print("✅ Отчет создан: sales_report_december.pdf")
```

**Результат:**
```
✅ PDF отчет создан
📊 Таблица: 5 строк данных
💰 Итого продаж: 985,000 ₽
📁 Файл: sales_report_december.pdf
```

---

## Пример 5: Разделение многостраничного PDF

### Команда:
```
Раздели договор на отдельные страницы
```

### Workflow:

```python
from pypdf import PdfReader, PdfWriter
from pathlib import Path

reader = PdfReader("contract_full.pdf")
output_dir = Path("contract_pages")
output_dir.mkdir(exist_ok=True)

for i, page in enumerate(reader.pages, start=1):
    writer = PdfWriter()
    writer.add_page(page)

    output_file = output_dir / f"page_{i:03d}.pdf"
    with open(output_file, "wb") as output:
        writer.write(output)

    print(f"✅ Создана страница {i}")

print(f"\n✅ Всего создано файлов: {len(reader.pages)}")
print(f"📁 Расположение: {output_dir}/")
```

**Результат:**
```
✅ Создано файлов: 8
📁 Расположение: contract_pages/
   page_001.pdf
   page_002.pdf
   ...
   page_008.pdf
```

---

## Пример 6: Добавление водяного знака

### Команда:
```
Добавь водяной знак "ЧЕРНОВИК" на все страницы отчета
```

### Workflow:

**Шаг 1 - Создание водяного знака:**
```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Создаем PDF с водяным знаком
c = canvas.Canvas("watermark.pdf", pagesize=letter)
c.setFont("Helvetica-Bold", 60)
c.setFillColorRGB(0.5, 0.5, 0.5, alpha=0.3)
c.saveState()
c.translate(300, 400)
c.rotate(45)
c.drawCentredString(0, 0, "ЧЕРНОВИК")
c.restoreState()
c.save()
```

**Шаг 2 - Наложение на документ:**
```python
from pypdf import PdfReader, PdfWriter

watermark = PdfReader("watermark.pdf").pages[0]
reader = PdfReader("report.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("report_draft.pdf", "wb") as output:
    writer.write(output)

print("✅ Водяной знак добавлен на все страницы")
```

**Результат:**
```
✅ Обработано страниц: 15
✅ Водяной знак: ЧЕРНОВИК (полупрозрачный, 45°)
📁 Создан файл: report_draft.pdf
```

---

## Пример 7: Извлечение изображений из PDF

### Команда:
```
Извлеки все изображения из презентации presentation.pdf
```

### Workflow:

```bash
# Используем pdfimages (poppler-utils)
mkdir presentation_images
pdfimages -j presentation.pdf presentation_images/img

ls presentation_images/
# img-000.jpg
# img-001.jpg
# img-002.png
# ...

echo "✅ Изображения извлечены"
```

**Альтернатива через Python:**
```python
from pypdf import PdfReader
from PIL import Image
import io

reader = PdfReader("presentation.pdf")
image_count = 0

for page_num, page in enumerate(reader.pages):
    if '/XObject' in page['/Resources']:
        xObject = page['/Resources']['/XObject'].get_object()

        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                data = xObject[obj].get_data()

                img = Image.open(io.BytesIO(data))
                img.save(f"img_page{page_num}_{image_count}.png")
                image_count += 1
                print(f"✅ Извлечено изображение {image_count}")

print(f"\n✅ Всего изображений: {image_count}")
```

**Результат:**
```
✅ Извлечено изображений: 23
📁 Расположение: presentation_images/
🖼️ Форматы: JPG (18), PNG (5)
```

---

## Советы по использованию

### ✅ Лучшие практики:

1. **Проверяй наличие текстового слоя**
   ```python
   text = page.extract_text()
   if not text.strip():
       print("Нужен OCR")
   ```

2. **Используй правильный инструмент**
   - Таблицы → pdfplumber
   - Базовые операции → pypdf
   - Создание PDF → reportlab
   - OCR → pytesseract

3. **Обрабатывай ошибки**
   ```python
   try:
       reader = PdfReader("file.pdf")
   except Exception as e:
       print(f"Ошибка: {e}")
   ```

### ⚠️ Частые проблемы:

**Проблема:** Таблицы извлекаются некорректно
**Решение:** Используй настройки pdfplumber для границ таблиц

**Проблема:** OCR не распознает кириллицу
**Решение:** Установи `tesseract-ocr-rus` и используй `lang='rus'`

**Проблема:** PDF защищен паролем
**Решение:** Используй `reader = PdfReader("file.pdf", password="pass")`
