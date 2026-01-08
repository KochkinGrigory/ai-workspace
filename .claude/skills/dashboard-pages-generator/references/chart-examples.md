# Примеры графиков для дашбордов

Готовые примеры на основе shadcn/ui Charts. **Используй их как основу, не пиши с нуля.**

---

## Правило выбора графика

| Тип данных | График |
|------------|--------|
| Сравнение категорий | Bar Chart |
| Несколько метрик по категориям | Stacked Bar |
| Воронка, рейтинги | Horizontal Bar |
| Тренды во времени | Line Chart |
| Тренды с акцентом на объем | Area Chart |
| Доли от целого | Pie/Donut |
| Прогресс, цели | Radial Bar |
| Многомерное сравнение | Radar |

---

## ChartConfig - обязательно для каждого графика

```tsx
const chartConfig = {
  keyName: {
    label: "Отображаемое название",
    color: "var(--chart-1)",  // CSS переменные из globals.css
  },
} satisfies ChartConfig;
```

Цвета в графиках через `var(--color-keyName)`.

---

## 1. Stacked Bar Chart

```tsx
const chartConfig = {
  revenue: { label: "Выручка", color: "var(--chart-1)" },
  expenses: { label: "Расходы", color: "var(--chart-2)" },
} satisfies ChartConfig;

<ChartContainer config={chartConfig} className="h-[300px] w-full">
  <BarChart data={data}>
    <CartesianGrid vertical={false} />
    <XAxis dataKey="month" tickLine={false} axisLine={false} />
    <ChartTooltip content={<ChartTooltipContent hideIndicator />} />
    <ChartLegend content={<ChartLegendContent />} />
    <Bar dataKey="revenue" stackId="a" fill="var(--color-revenue)" radius={[0, 0, 4, 4]} />
    <Bar dataKey="expenses" stackId="a" fill="var(--color-expenses)" radius={[4, 4, 0, 0]} />
  </BarChart>
</ChartContainer>
```

---

## 2. Area Chart с градиентом

```tsx
<ChartContainer config={chartConfig} className="h-[300px] w-full">
  <AreaChart data={data}>
    <defs>
      <linearGradient id="fillDesktop" x1="0" y1="0" x2="0" y2="1">
        <stop offset="5%" stopColor="var(--color-desktop)" stopOpacity={0.8} />
        <stop offset="95%" stopColor="var(--color-desktop)" stopOpacity={0.1} />
      </linearGradient>
    </defs>
    <CartesianGrid vertical={false} />
    <XAxis dataKey="month" tickLine={false} axisLine={false} />
    <ChartTooltip cursor={false} content={<ChartTooltipContent indicator="line" />} />
    <Area
      dataKey="desktop"
      type="natural"
      fill="url(#fillDesktop)"
      stroke="var(--color-desktop)"
    />
  </AreaChart>
</ChartContainer>
```

---

## 3. Donut Chart с центральным текстом

```tsx
import { Label } from "recharts";

<ChartContainer config={chartConfig} className="mx-auto aspect-square max-h-[300px]">
  <PieChart>
    <ChartTooltip cursor={false} content={<ChartTooltipContent hideLabel />} />
    <Pie data={data} dataKey="value" nameKey="category" innerRadius={60}>
      <Label
        content={({ viewBox }) => {
          if (viewBox && "cx" in viewBox && "cy" in viewBox) {
            return (
              <text x={viewBox.cx} y={viewBox.cy} textAnchor="middle">
                <tspan x={viewBox.cx} y={viewBox.cy} className="fill-foreground text-3xl font-bold">
                  {total}
                </tspan>
                <tspan x={viewBox.cx} y={(viewBox.cy || 0) + 24} className="fill-muted-foreground">
                  Total
                </tspan>
              </text>
            );
          }
        }}
      />
    </Pie>
  </PieChart>
</ChartContainer>
```

---

## 4. Horizontal Bar Chart

```tsx
<ChartContainer config={chartConfig} className="h-[300px] w-full">
  <BarChart data={data} layout="vertical">
    <CartesianGrid horizontal={false} />
    <YAxis
      dataKey="stage"
      type="category"
      tickLine={false}
      axisLine={false}
      width={120}
    />
    <XAxis type="number" hide />
    <ChartTooltip content={<ChartTooltipContent />} />
    <Bar dataKey="count" fill="var(--color-count)" radius={[0, 4, 4, 0]} />
  </BarChart>
</ChartContainer>
```

---

## 5. Line Chart с точками

```tsx
<ChartContainer config={chartConfig} className="h-[300px] w-full">
  <LineChart data={data}>
    <CartesianGrid vertical={false} />
    <XAxis dataKey="month" tickLine={false} axisLine={false} />
    <ChartTooltip cursor={false} content={<ChartTooltipContent />} />
    <Line
      dataKey="users"
      type="monotone"
      stroke="var(--color-users)"
      strokeWidth={2}
      dot={{ fill: "var(--color-users)", r: 4 }}
      activeDot={{ r: 6 }}
    />
  </LineChart>
</ChartContainer>
```

---

## 6. Radial Bar Chart

```tsx
import { RadialBar, RadialBarChart } from "recharts";

const data = [
  { name: "Chrome", value: 275, fill: "var(--chart-1)" },
  { name: "Safari", value: 200, fill: "var(--chart-2)" },
];

<ChartContainer config={chartConfig} className="mx-auto aspect-square max-h-[300px]">
  <RadialBarChart data={data} innerRadius={30} outerRadius={110}>
    <ChartTooltip cursor={false} content={<ChartTooltipContent hideLabel />} />
    <RadialBar dataKey="value" background />
  </RadialBarChart>
</ChartContainer>
```

---

## 7. Radar Chart

```tsx
import { PolarAngleAxis, PolarGrid, Radar, RadarChart } from "recharts";

<ChartContainer config={chartConfig} className="mx-auto aspect-square max-h-[300px]">
  <RadarChart data={data}>
    <ChartTooltip cursor={false} content={<ChartTooltipContent />} />
    <PolarAngleAxis dataKey="subject" />
    <PolarGrid />
    <Radar dataKey="value" fill="var(--color-value)" fillOpacity={0.6} />
  </RadarChart>
</ChartContainer>
```

---

## Импорты

```tsx
"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Bar, BarChart, CartesianGrid, XAxis, Area, AreaChart, Line, LineChart, Pie, PieChart } from "recharts";
import {
  ChartConfig,
  ChartContainer,
  ChartLegend,
  ChartLegendContent,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";
import { TrendingUp, Users, UserCheck, Percent, DollarSign } from "lucide-react";
```

---

## Ресурсы

Только для редких случаев: https://ui.shadcn.com/charts
