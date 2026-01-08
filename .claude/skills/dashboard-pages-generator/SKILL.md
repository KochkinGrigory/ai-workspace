---
name: dashboard-pages-generator
description: Создание интерактивных дашбордов с данными из БД. Используй когда нужны графики, таблицы, визуализация метрик. Результат - Next.js страница на https://my-jarvis.ru/dashboard/[name].
allowed-tools: Read, Write, Edit, Bash(cmd:*), Bash(docker*), mcp__buisness-database-analiticalo__query
version: 1.1.0
---

# Dashboard Pages Generator

Создание веб-дашбордов с визуализацией данных через Next.js + Recharts.

---

## Когда использовать

**ВСЕГДА при запросах на визуализацию:**
- "Создай дашборд/отчет/визуализацию"
- "Покажи данные на графике/в таблице"
- "Визуализируй статистику/метрики"
- "Построй график конверсий/продаж"

**НЕ использовать для:**
- Сайтов/лендингов без данных → `website-pages-generator`
- Текстового анализа без графиков

**Правило:** Данные + Графики = этот skill. Дизайн + Анимации = website-pages-generator.

---

## Технический стек

- **Проект:** `/opt/ai-workspace/apps/dashboard-pages/frontend`
- **URL:** `https://my-jarvis.ru/dashboard/[report-name]`
- **Технологии:** Next.js 15, TypeScript, Tailwind CSS, Recharts, shadcn UI
- **Деплой:** Docker (порт 3001)

---

## Workflow создания дашборда

### 1. Получить данные

Использовать `mcp__buisness-database-analiticalo__query` для SQL-запросов.

### 2. Создать страницу

**Путь:** `apps/dashboard-pages/frontend/src/app/[report-name]/page.tsx`

```tsx
"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Bar, BarChart, CartesianGrid, XAxis } from "recharts";
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";

const data = [/* данные из БД */];

const chartConfig = {
  value: { label: "Значение", color: "var(--chart-1)" },
} satisfies ChartConfig;

export default function ReportName() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="border-b bg-card">
        <div className="container mx-auto px-4 md:px-6 py-4 md:py-6">
          <h1 className="text-2xl md:text-3xl font-bold">Название</h1>
        </div>
      </div>

      {/* Content */}
      <div className="container mx-auto px-4 md:px-6 py-6 md:py-8">
        {/* Metric Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Метрика</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">123</div>
            </CardContent>
          </Card>
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>График</CardTitle>
            </CardHeader>
            <CardContent>
              <ChartContainer config={chartConfig} className="h-[300px] w-full">
                <BarChart data={data}>
                  <CartesianGrid vertical={false} />
                  <XAxis dataKey="name" tickLine={false} axisLine={false} />
                  <ChartTooltip content={<ChartTooltipContent />} />
                  <Bar dataKey="value" fill="var(--color-value)" radius={4} />
                </BarChart>
              </ChartContainer>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
```

### 3. ОБЯЗАТЕЛЬНО перезапустить Docker

```bash
cd /opt/ai-workspace/apps/dashboard-pages && docker-compose restart
```

**БЕЗ ЭТОГО СТРАНИЦА НЕ БУДЕТ РАБОТАТЬ (404)!**

### 4. Проверить и вернуть ссылку

```bash
curl -I https://my-jarvis.ru/dashboard/[report-name]
# Должен вернуть 200
```

**Ответ пользователю:**
```
Дашборд создан: https://my-jarvis.ru/dashboard/[report-name]
```

**Для Telegram:**
```bash
/tg "✅ <b>Дашборд создан!</b>

📊 <a href=\"https://my-jarvis.ru/dashboard/[name]\">Открыть дашборд</a>"
```

---

## Удаление дашборда

```bash
rm -rf /opt/ai-workspace/apps/dashboard-pages/frontend/src/app/[report-name]
cd /opt/ai-workspace/apps/dashboard-pages && docker-compose restart
```

---

## Ключевые правила

### ВСЕГДА:
- ✅ `"use client";` в начале файла
- ✅ Данные hardcoded в компоненте (не fetch)
- ✅ ChartContainer вместо ResponsiveContainer
- ✅ ChartConfig для каждого графика
- ✅ Адаптивный дизайн (см. `references/responsive-design.md`)
- ✅ Перезапуск Docker после изменений
- ✅ Проверка curl перед отправкой ссылки

### НИКОГДА:
- ❌ npm напрямую (только Docker)
- ❌ Трогать layout.tsx и globals.css
- ❌ API endpoints (данные hardcoded)
- ❌ Вложенные структуры папок

---

## References

Подробная документация в `references/`:

- **chart-examples.md** - примеры всех типов графиков (Bar, Line, Area, Pie, Radar)
- **responsive-design.md** - адаптивность и Tailwind breakpoints
- **troubleshooting.md** - решение проблем (404, порт занят и т.д.)

---

## Архитектура

```
apps/dashboard-pages/
├── frontend/
│   ├── src/app/
│   │   ├── layout.tsx         # НЕ ТРОГАТЬ
│   │   ├── globals.css        # НЕ ТРОГАТЬ
│   │   ├── october-2025/      # Пример отчета
│   │   │   └── page.tsx
│   │   └── [report-name]/     # Новые отчеты
│   │       └── page.tsx
│   └── components/ui/         # shadcn компоненты
└── docker-compose.yml
```

**Принцип:** Каждый дашборд = папка в `src/app/[name]/page.tsx`

---

## Интеграция с analiticalo-db-analytics

Для данных из БД клиники:
1. Читай `analiticalo-db-analytics/references/facts-and-business-logic.md`
2. Уникальность клиентов по полю `phone`
3. Конверсия = `appointment_scheduled = true OR cancellation_reason = 'Записали в журнале записи'`

---

## Brands (опционально)

Брендовые ресурсы в `brands/` → `/opt/ai-workspace/assets/brands/`

Для фирменных цветов графиков:
1. Читай `brands/[бренд]/guidelines/colors.txt`
2. Применяй в ChartConfig

---

**Версия:** 1.1.0
**URL:** https://my-jarvis.ru/dashboard
