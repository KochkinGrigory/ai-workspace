# Адаптивный дизайн дашбордов

Mobile-first подход с Tailwind CSS breakpoints.

---

## Tailwind Breakpoints

| Префикс | Размер | Устройство |
|---------|--------|------------|
| (без) | < 640px | Mobile |
| `sm:` | ≥ 640px | Small tablets |
| `md:` | ≥ 768px | Tablets |
| `lg:` | ≥ 1024px | Desktop |
| `xl:` | ≥ 1280px | Large desktop |

---

## Типичные паттерны

### Сетка метрик
```tsx
// 1 колонка на mobile, 2 на tablet, 4 на desktop
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
```

### Сетка графиков
```tsx
// 1 колонка на mobile, 2 на desktop
<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
```

### Адаптивные заголовки
```tsx
<h1 className="text-2xl md:text-3xl lg:text-4xl font-bold">
```

### Адаптивные отступы
```tsx
<div className="px-4 md:px-6 lg:px-8 py-4 md:py-6 lg:py-8">
```

### Контейнер с адаптивными отступами
```tsx
<div className="container mx-auto px-4 md:px-6">
```

---

## Таблицы с горизонтальной прокруткой

```tsx
<div className="overflow-x-auto -mx-2 md:mx-0">
  <table className="w-full min-w-[600px]">
    <thead>
      <tr className="border-b">
        <th className="text-left p-2 md:p-4 font-medium text-sm">Колонка</th>
      </tr>
    </thead>
    <tbody>
      {/* rows */}
    </tbody>
  </table>
</div>
```

---

## Графики

Всегда используй `className="h-[300px] w-full"` для ChartContainer:

```tsx
<ChartContainer config={chartConfig} className="h-[300px] w-full">
```

---

## Чеклист

- ✅ Метрики в 1 колонку на телефонах
- ✅ Графики корректно на узких экранах
- ✅ Таблицы прокручиваются горизонтально
- ✅ Текст читаем на маленьких экранах
- ✅ Отступы не слишком большие на mobile
