# Цветовая система дашбордов

Официальная цветовая схема shadcn/ui для графиков (OKLCH формат).

---

## Палитра графиков

### Light Mode (:root)

| Переменная | OKLCH | Визуально |
|------------|-------|-----------|
| `--chart-1` | `oklch(0.646 0.222 41.116)` | Orange/Coral |
| `--chart-2` | `oklch(0.6 0.118 184.704)` | Teal |
| `--chart-3` | `oklch(0.398 0.07 227.392)` | Dark Blue |
| `--chart-4` | `oklch(0.828 0.189 84.429)` | Yellow/Gold |
| `--chart-5` | `oklch(0.769 0.188 70.08)` | Light Orange |

### Dark Mode (.dark)

| Переменная | OKLCH | Визуально |
|------------|-------|-----------|
| `--chart-1` | `oklch(0.488 0.243 264.376)` | Blue |
| `--chart-2` | `oklch(0.696 0.17 162.48)` | Green |
| `--chart-3` | `oklch(0.769 0.188 70.08)` | Orange |
| `--chart-4` | `oklch(0.627 0.265 303.9)` | Purple |
| `--chart-5` | `oklch(0.645 0.246 16.439)` | Red/Pink |

---

## Правила использования в коде

### ПРАВИЛЬНО

```tsx
// В chartConfig
const chartConfig = {
  revenue: {
    label: "Выручка",
    color: "var(--chart-1)",  // Ссылка на CSS переменную
  },
} satisfies ChartConfig;

// В компоненте (через --color-{key})
<Bar fill="var(--color-revenue)" />
<Line stroke="var(--color-revenue)" />

// В данных для Pie/Radial (через --color-{key})
const data = [
  { name: "Chrome", value: 275, fill: "var(--color-chrome)" },
];
```

### НЕПРАВИЛЬНО

```tsx
// НЕ оборачивай в hsl() или oklch() - переменная УЖЕ содержит полное значение
color: "hsl(var(--chart-1))"    // ОШИБКА!
color: "oklch(var(--chart-1))"  // ОШИБКА!

// НЕ используй прямые ссылки в данных Pie
fill: "var(--chart-1)"  // ОШИБКА! Нужно через config
```

---

## Паттерн для Pie/Radial Charts

Pie и Radial требуют особого паттерна с именованными ключами:

```tsx
// 1. Данные с fill через --color-{key}
const chartData = [
  { browser: "chrome", visitors: 275, fill: "var(--color-chrome)" },
  { browser: "safari", visitors: 200, fill: "var(--color-safari)" },
  { browser: "firefox", visitors: 187, fill: "var(--color-firefox)" },
];

// 2. Config с именованными ключами
const chartConfig = {
  visitors: { label: "Visitors" },
  chrome: { label: "Chrome", color: "var(--chart-1)" },
  safari: { label: "Safari", color: "var(--chart-2)" },
  firefox: { label: "Firefox", color: "var(--chart-3)" },
} satisfies ChartConfig;

// 3. Компонент
<Pie data={chartData} dataKey="visitors" />
<ChartLegend content={<ChartLegendContent nameKey="browser" />} />
```

---

## Паттерн для Line/Bar/Area Charts

```tsx
// 1. Config
const chartConfig = {
  desktop: { label: "Desktop", color: "var(--chart-1)" },
  mobile: { label: "Mobile", color: "var(--chart-2)" },
} satisfies ChartConfig;

// 2. Компонент - ссылка через --color-{key}
<Line dataKey="desktop" stroke="var(--color-desktop)" />
<Bar dataKey="mobile" fill="var(--color-mobile)" />
<Area dataKey="desktop" fill="var(--color-desktop)" stroke="var(--color-desktop)" />
```

---

## Полный globals.css (официальные значения shadcn/ui)

```css
@layer base {
  :root {
    --chart-1: oklch(0.646 0.222 41.116);
    --chart-2: oklch(0.6 0.118 184.704);
    --chart-3: oklch(0.398 0.07 227.392);
    --chart-4: oklch(0.828 0.189 84.429);
    --chart-5: oklch(0.769 0.188 70.08);
  }

  .dark {
    --chart-1: oklch(0.488 0.243 264.376);
    --chart-2: oklch(0.696 0.17 162.48);
    --chart-3: oklch(0.769 0.188 70.08);
    --chart-4: oklch(0.627 0.265 303.9);
    --chart-5: oklch(0.645 0.246 16.439);
  }
}
```

---

## Частые ошибки

### 1. Обертка hsl()/oklch()
```tsx
// НЕПРАВИЛЬНО - черные графики
color: "hsl(var(--chart-1))"
color: "oklch(var(--chart-1))"

// ПРАВИЛЬНО
color: "var(--chart-1)"
```

### 2. Прямые ссылки в Pie данных
```tsx
// НЕПРАВИЛЬНО - цвета не применятся
{ name: "A", value: 10, fill: "var(--chart-1)" }

// ПРАВИЛЬНО - через config
{ category: "a", name: "A", value: 10, fill: "var(--color-a)" }
// + в config: a: { color: "var(--chart-1)" }
```

### 3. Разные масштабы на одном графике
```tsx
// НЕПРАВИЛЬНО - orders будут "прижаты" к нулю
<Line dataKey="revenue" />  // 45000-89000
<Line dataKey="orders" />   // 120-268

// ПРАВИЛЬНО - интерактивный переключатель
const [activeChart, setActiveChart] = useState("revenue");
<Line dataKey={activeChart} stroke={`var(--color-${activeChart})`} />
```

---

## Источник

Официальная документация: https://ui.shadcn.com/docs/components/chart
