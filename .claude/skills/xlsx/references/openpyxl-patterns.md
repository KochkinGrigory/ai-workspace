# Паттерны работы с openpyxl и pandas

Подробные примеры и лучшие практики для работы с Excel файлами.

## Выбор библиотеки

- **pandas**: Лучше всего для анализа данных, массовых операций и простого экспорта данных
- **openpyxl**: Лучше всего для сложного форматирования, формул и специфичных для Excel функций

## Чтение и анализ данных

### Анализ данных с pandas

Для анализа данных, визуализации и базовых операций используйте **pandas**:

```python
import pandas as pd

# Read Excel
df = pd.read_excel('file.xlsx')  # Default: first sheet
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # All sheets as dict

# Analyze
df.head()      # Preview data
df.info()      # Column info
df.describe()  # Statistics

# Write Excel
df.to_excel('output.xlsx', index=False)
```

### Работа с pandas - лучшие практики

```python
# Указывать типы данных
pd.read_excel('file.xlsx', dtype={'id': str, 'amount': float})

# Для больших файлов читать конкретные столбцы
pd.read_excel('file.xlsx', usecols=['A', 'C', 'E'])

# Правильно обрабатывать даты
pd.read_excel('file.xlsx', parse_dates=['date_column'])

# Читать конкретный лист
pd.read_excel('file.xlsx', sheet_name='Sheet2')
```

## Создание новых файлов Excel

### Базовое создание с openpyxl

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active

# Add data
sheet['A1'] = 'Hello'
sheet['B1'] = 'World'
sheet.append(['Row', 'of', 'data'])

# Add formula
sheet['B2'] = '=SUM(A1:A10)'

# Formatting
sheet['A1'].font = Font(bold=True, color='FF0000')
sheet['A1'].fill = PatternFill('solid', start_color='FFFF00')
sheet['A1'].alignment = Alignment(horizontal='center')

# Column width
sheet.column_dimensions['A'].width = 20

wb.save('output.xlsx')
```

### Создание таблицы с данными из pandas

```python
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

# Prepare data
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# Create workbook
wb = Workbook()
sheet = wb.active

# Write dataframe to sheet
for r in dataframe_to_rows(df, index=False, header=True):
    sheet.append(r)

wb.save('output.xlsx')
```

## Редактирование существующих файлов

### Загрузка и модификация

```python
from openpyxl import load_workbook

# Load existing file
wb = load_workbook('existing.xlsx')
sheet = wb.active  # or wb['SheetName'] for specific sheet

# Working with multiple sheets
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    print(f"Sheet: {sheet_name}")

# Modify cells
sheet['A1'] = 'New Value'
sheet.insert_rows(2)  # Insert row at position 2
sheet.delete_cols(3)  # Delete column 3

# Add new sheet
new_sheet = wb.create_sheet('NewSheet')
new_sheet['A1'] = 'Data'

wb.save('modified.xlsx')
```

### Чтение вычисленных значений

```python
from openpyxl import load_workbook

# Load with data_only=True to read calculated values
wb = load_workbook('file.xlsx', data_only=True)
sheet = wb.active

# Now cells contain values instead of formulas
value = sheet['B2'].value  # Gets calculated value, not '=SUM(A1:A10)'

# ВАЖНО: Если сохранить с data_only=True, формулы будут потеряны!
# Поэтому используй data_only=True только для чтения
```

### Работа с большими файлами

```python
from openpyxl import load_workbook

# Read-only mode для больших файлов
wb = load_workbook('large_file.xlsx', read_only=True)
sheet = wb.active

for row in sheet.iter_rows(min_row=1, max_row=1000, values_only=True):
    print(row)

wb.close()

# Write-only mode для создания больших файлов
from openpyxl import Workbook

wb = Workbook(write_only=True)
ws = wb.create_sheet()

for row in range(10000):
    ws.append([f'Data {row}', row * 2, row * 3])

wb.save('large_output.xlsx')
```

## КРИТИЧЕСКИ ВАЖНО: Использовать формулы, а не жестко закодированные значения

**Всегда используйте формулы Excel вместо вычисления значений в Python и их жесткого кодирования.**

### ❌ НЕПРАВИЛЬНО - Жесткое кодирование вычисленных значений

```python
# Bad: Calculating in Python and hardcoding result
total = df['Sales'].sum()
sheet['B10'] = total  # Hardcodes 5000

# Bad: Computing growth rate in Python
growth = (df.iloc[-1]['Revenue'] - df.iloc[0]['Revenue']) / df.iloc[0]['Revenue']
sheet['C5'] = growth  # Hardcodes 0.15

# Bad: Python calculation for average
avg = sum(values) / len(values)
sheet['D20'] = avg  # Hardcodes 42.5
```

### ✅ ПРАВИЛЬНО - Использование формул Excel

```python
# Good: Let Excel calculate the sum
sheet['B10'] = '=SUM(B2:B9)'

# Good: Growth rate as Excel formula
sheet['C5'] = '=(C4-C2)/C2'

# Good: Average using Excel function
sheet['D20'] = '=AVERAGE(D2:D19)'
```

## Работа с форматированием

### Стили ячеек

```python
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment

# Font
cell.font = Font(
    name='Arial',
    size=12,
    bold=True,
    italic=False,
    color='FF0000'  # Red
)

# Fill (background color)
cell.fill = PatternFill(
    fill_type='solid',
    start_color='FFFF00'  # Yellow
)

# Border
thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)
cell.border = thin_border

# Alignment
cell.alignment = Alignment(
    horizontal='center',  # 'left', 'center', 'right'
    vertical='center',    # 'top', 'center', 'bottom'
    wrap_text=True
)
```

### Форматирование чисел

```python
# Currency
cell.number_format = '$#,##0.00'

# Percentage
cell.number_format = '0.0%'

# Date
cell.number_format = 'yyyy-mm-dd'

# Custom (zeros as dash)
cell.number_format = '$#,##0;($#,##0);-'
```

### Ширина столбцов и высота строк

```python
# Set column width
sheet.column_dimensions['A'].width = 20

# Set row height
sheet.row_dimensions[1].height = 30

# Auto-fit column width (approximate)
from openpyxl.utils import get_column_letter

for col in range(1, sheet.max_column + 1):
    column_letter = get_column_letter(col)
    max_length = 0
    for cell in sheet[column_letter]:
        if cell.value:
            max_length = max(max_length, len(str(cell.value)))
    sheet.column_dimensions[column_letter].width = max_length + 2
```

### Замораживание областей

```python
# Freeze first row (header)
sheet.freeze_panes = 'A2'

# Freeze first column
sheet.freeze_panes = 'B1'

# Freeze first row and first column
sheet.freeze_panes = 'B2'
```

## Работа с формулами

### Простые формулы

```python
# SUM
sheet['A10'] = '=SUM(A1:A9)'

# AVERAGE
sheet['B10'] = '=AVERAGE(B1:B9)'

# COUNT
sheet['C10'] = '=COUNT(C1:C9)'

# IF
sheet['D10'] = '=IF(A10>100, "High", "Low")'
```

### Формулы с абсолютными ссылками

```python
# Relative reference (changes when copied)
sheet['B2'] = '=A2*2'

# Absolute reference (stays fixed when copied)
sheet['B2'] = '=$A$1*A2'

# Mixed reference
sheet['B2'] = '=$A2*B$1'
```

### Межлистовые ссылки

```python
# Reference to another sheet
sheet['A1'] = '=Sheet2!B5'

# Reference to range in another sheet
sheet['A1'] = '=SUM(Sheet2!A1:A10)'
```

## Важные замечания для openpyxl

- **Индексы ячеек основаны на 1**: row=1, column=1 относится к ячейке A1
- **Формулы сохраняются, но не вычисляются**: использовать `scripts/recalc.py` для обновления значений
- **data_only=True опасно**: Если открыто с `data_only=True` и сохранено, формулы заменяются значениями и теряются навсегда
- **Для больших файлов**: Использовать `read_only=True` для чтения или `write_only=True` для записи

## Руководящие принципы стиля кода

**ВАЖНО**: При генерации кода Python для операций с Excel:
- Писать минимальный, краткий код Python без ненужных комментариев
- Избегать многословных имен переменных и избыточных операций
- Избегать ненужных операторов print

**Для самих файлов Excel**:
- Добавлять комментарии к ячейкам со сложными формулами или важными предположениями
- Документировать источники данных для жестко закодированных значений
- Включать примечания для ключевых вычислений и разделов модели

## Поиск информации

```bash
# Найти про работу с pandas
grep -A 10 "pandas" references/openpyxl-patterns.md

# Найти про форматирование
grep -A 10 "Форматирование" references/openpyxl-patterns.md

# Найти про формулы
grep -A 10 "формулами" references/openpyxl-patterns.md
```
