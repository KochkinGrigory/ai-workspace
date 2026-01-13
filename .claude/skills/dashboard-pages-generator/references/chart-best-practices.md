# Best Practices для информативных графиков

Правила создания читаемых и информативных графиков.

---

## Обязательные элементы

### 1. Оси с подписями

```tsx
// ПРАВИЛЬНО - оси видимы и понятны
<XAxis
  dataKey="month"
  tickLine={false}
  axisLine={false}
  tickMargin={8}
/>
<YAxis
  tickLine={false}
  axisLine={false}
  tickMargin={8}
  tickFormatter={(value) => `${(value / 1000).toFixed(0)}k`}  // Форматирование!
/>

// НЕПРАВИЛЬНО - скрытые оси
<YAxis hide />  // Пользователь не видит масштаб!
```

### 2. Сетка для читаемости

```tsx
// Пунктирная сетка помогает читать значения
<CartesianGrid strokeDasharray="3 3" />

// Или только горизонтальные линии
<CartesianGrid vertical={false} />
```

### 3. Подписи значений на точках/барах

```tsx
// Line chart с подписями
<Line dataKey="value" ...>
  <LabelList
    dataKey="value"
    position="top"
    offset={10}
    className="fill-foreground"
    fontSize={10}
    formatter={(value: number) => `${(value / 1000).toFixed(0)}k`}
  />
</Line>

// Bar chart с подписями
<Bar dataKey="revenue" ...>
  <LabelList
    dataKey="revenue"
    position="right"
    offset={8}
    formatter={(value: number) => `${(value / 1000).toFixed(0)}k ₽`}
  />
</Bar>
```

### 4. Информативный Tooltip

```tsx
<ChartTooltip
  content={
    <ChartTooltipContent
      className="w-[180px]"
      labelFormatter={(value) => value}
      formatter={(value, name) => {
        const numValue = Number(value);
        if (name === "sales") {
          return [`${numValue.toLocaleString('ru-RU')} ₽`, "Выручка"];
        }
        return [`${numValue.toLocaleString('ru-RU')} шт`, "Заказы"];
      }}
    />
  }
/>
```

---

## Форматирование чисел

### Большие числа

```tsx
// Тысячи -> "45k"
formatter={(value) => `${(value / 1000).toFixed(0)}k`}

// Миллионы -> "1.2M"
formatter={(value) => `${(value / 1000000).toFixed(1)}M`}

// С разделителями -> "1 234 567"
formatter={(value) => value.toLocaleString('ru-RU')}
```

### Валюта

```tsx
// Краткое -> "45k ₽"
formatter={(value) => `${(value / 1000).toFixed(0)}k ₽`}

// Полное -> "45 000 ₽"
formatter={(value) => `${value.toLocaleString('ru-RU')} ₽`}
```

### Проценты

```tsx
formatter={(value) => `${value}%`}
```

---

## Метрики с разным масштабом

### НЕПРАВИЛЬНО - две метрики на одном графике

```tsx
// Выручка 45000-89000 и заказы 120-268 на одной оси
// Заказы будут выглядеть как плоская линия у нуля!
<Line dataKey="revenue" />
<Line dataKey="orders" />
```

### ПРАВИЛЬНО - интерактивный переключатель

```tsx
const [activeChart, setActiveChart] = useState<"revenue" | "orders">("revenue");

// Кнопки переключения
<div className="flex">
  {(["revenue", "orders"] as const).map((key) => (
    <button
      key={key}
      data-active={activeChart === key}
      className="data-[active=true]:bg-muted/50 flex flex-col px-6 py-4 border-l"
      onClick={() => setActiveChart(key)}
    >
      <span className="text-xs text-muted-foreground">{config[key].label}</span>
      <span className="text-2xl font-bold">{formatValue(totals[key])}</span>
    </button>
  ))}
</div>

// Один график с динамическим dataKey
<Line
  dataKey={activeChart}
  stroke={`var(--color-${activeChart})`}
/>

// YAxis с динамическим форматированием
<YAxis
  tickFormatter={(value) =>
    activeChart === "revenue" ? `${(value / 1000).toFixed(0)}k` : value
  }
/>
```

---

## Layout метрик-карточек

### НЕПРАВИЛЬНО - переполнение и перенос

```tsx
// Метка "Выручка ₽" + значение "790 000 ₽" = дублирование символа
<CardTitle>Выручка ₽</CardTitle>
<div>790 000 ₽</div>

// Обычный пробел перед ₽ - может перенестись на новую строку!
<span>{value}M ₽</span>  // "6.48M" и "₽" на разных строках
```

### ПРАВИЛЬНО - чистый layout

```tsx
// Вариант 1: Символ только в значении
<CardTitle className="text-sm text-muted-foreground">Общая выручка</CardTitle>
<div className="text-2xl font-bold">{value.toLocaleString('ru-RU')} ₽</div>

// Вариант 2: Символ только в заголовке
<CardTitle>Выручка, ₽</CardTitle>
<div className="text-2xl font-bold">{value.toLocaleString('ru-RU')}</div>

// Вариант 3: Non-breaking space + whitespace-nowrap
<span className="whitespace-nowrap">{value}M\u00A0₽</span>  // Никогда не переносится!
```

### Правило для чисел с единицами измерения

```tsx
// ВСЕГДА используй \u00A0 (non-breaking space) между числом и единицей
`${value}\u00A0₽`     // 1 234₽ - не разорвётся
`${value}\u00A0шт`    // 100 шт - не разорвётся
`${value}\u00A0%`     // 15.5% - не разорвётся

// ИЛИ добавляй whitespace-nowrap на контейнер
<span className="whitespace-nowrap">{value} ₽</span>
```

---

## Высота графиков

```tsx
// Минимальная высота для читаемости
className="h-[300px] w-full"

// Для графиков с большим количеством данных
className="h-[400px] w-full"

// Адаптивная высота
className="aspect-auto h-[300px] w-full"
```

---

## Margin для подписей

```tsx
// Если есть LabelList сверху - добавь top margin
<LineChart margin={{ left: 12, right: 12, top: 20 }}>

// Если есть LabelList справа - добавь right margin
<BarChart margin={{ right: 50 }}>
```

---

## Dot styling

```tsx
// Видимые точки на линии
<Line
  dot={{ r: 4, fill: "var(--color-dataKey)" }}
  activeDot={{ r: 6 }}  // Увеличенная при наведении
/>

// Без точек (для большого количества данных)
<Line dot={false} />
```

---

## Checklist перед деплоем

- [ ] Оси подписаны и форматированы
- [ ] Сетка видима (CartesianGrid)
- [ ] Tooltip показывает понятные значения с единицами измерения
- [ ] Подписи значений на точках/барах (LabelList)
- [ ] Нет переполнения текста
- [ ] Разные масштабы - на разных графиках или с переключателем
- [ ] Margin достаточен для подписей
