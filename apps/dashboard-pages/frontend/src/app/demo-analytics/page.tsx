"use client";

import * as React from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  CardFooter,
} from "@/components/ui/card";
import {
  Bar,
  BarChart,
  CartesianGrid,
  XAxis,
  YAxis,
  Line,
  LineChart,
  Pie,
  PieChart,
  Area,
  AreaChart,
  RadialBar,
  RadialBarChart,
  PolarGrid,
  PolarRadiusAxis,
  Label,
  LabelList,
} from "recharts";
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  ChartLegend,
  ChartLegendContent,
} from "@/components/ui/chart";
import { TrendingUp, TrendingDown, Users, ShoppingCart, DollarSign, Package } from "lucide-react";

// ==================== ДАННЫЕ ====================

// Ежедневные продажи за последние 30 дней
const dailySalesData = [
  { date: "01.12", revenue: 145000, orders: 42, visitors: 1250 },
  { date: "02.12", revenue: 132000, orders: 38, visitors: 1180 },
  { date: "03.12", revenue: 168000, orders: 51, visitors: 1420 },
  { date: "04.12", revenue: 155000, orders: 45, visitors: 1350 },
  { date: "05.12", revenue: 189000, orders: 58, visitors: 1580 },
  { date: "06.12", revenue: 201000, orders: 62, visitors: 1720 },
  { date: "07.12", revenue: 178000, orders: 54, visitors: 1490 },
  { date: "08.12", revenue: 165000, orders: 48, visitors: 1380 },
  { date: "09.12", revenue: 142000, orders: 41, visitors: 1220 },
  { date: "10.12", revenue: 198000, orders: 59, visitors: 1650 },
  { date: "11.12", revenue: 215000, orders: 67, visitors: 1820 },
  { date: "12.12", revenue: 228000, orders: 72, visitors: 1950 },
  { date: "13.12", revenue: 195000, orders: 58, visitors: 1680 },
  { date: "14.12", revenue: 182000, orders: 55, visitors: 1520 },
  { date: "15.12", revenue: 210000, orders: 65, visitors: 1780 },
  { date: "16.12", revenue: 235000, orders: 74, visitors: 2010 },
  { date: "17.12", revenue: 248000, orders: 78, visitors: 2150 },
  { date: "18.12", revenue: 220000, orders: 68, visitors: 1890 },
  { date: "19.12", revenue: 205000, orders: 63, visitors: 1750 },
  { date: "20.12", revenue: 192000, orders: 57, visitors: 1620 },
  { date: "21.12", revenue: 268000, orders: 85, visitors: 2320 },
  { date: "22.12", revenue: 285000, orders: 92, visitors: 2480 },
  { date: "23.12", revenue: 312000, orders: 98, visitors: 2720 },
  { date: "24.12", revenue: 345000, orders: 112, visitors: 3050 },
  { date: "25.12", revenue: 128000, orders: 35, visitors: 980 },
  { date: "26.12", revenue: 298000, orders: 95, visitors: 2650 },
  { date: "27.12", revenue: 275000, orders: 88, visitors: 2420 },
  { date: "28.12", revenue: 258000, orders: 82, visitors: 2280 },
  { date: "29.12", revenue: 242000, orders: 76, visitors: 2120 },
  { date: "30.12", revenue: 265000, orders: 84, visitors: 2350 },
];

// Продажи по категориям
const categoryData = [
  { category: "electronics", name: "Электроника", value: 2850000, fill: "var(--color-electronics)" },
  { category: "clothing", name: "Одежда", value: 1920000, fill: "var(--color-clothing)" },
  { category: "home", name: "Дом и сад", value: 1450000, fill: "var(--color-home)" },
  { category: "sports", name: "Спорт", value: 980000, fill: "var(--color-sports)" },
  { category: "beauty", name: "Красота", value: 720000, fill: "var(--color-beauty)" },
];

// Топ-10 товаров
const topProductsData = [
  { product: "iPhone 15 Pro", revenue: 1245000, units: 415 },
  { product: "Samsung S24 Ultra", revenue: 989000, units: 342 },
  { product: "MacBook Air M3", revenue: 876000, units: 219 },
  { product: "AirPods Pro 2", revenue: 654000, units: 872 },
  { product: "PlayStation 5", revenue: 598000, units: 199 },
  { product: "Nike Air Max", revenue: 445000, units: 593 },
  { product: "iPad Pro 12.9", revenue: 412000, units: 137 },
  { product: "Dyson V15", revenue: 387000, units: 129 },
  { product: "Apple Watch 9", revenue: 356000, units: 356 },
  { product: "Sony WH-1000XM5", revenue: 298000, units: 398 },
];

// Конверсия воронки
const funnelData = [
  { stage: "Посетители", value: 52840, fill: "var(--color-visitors)" },
  { stage: "Просмотр товара", value: 31704, fill: "var(--color-views)" },
  { stage: "Добавление в корзину", value: 12682, fill: "var(--color-cart)" },
  { stage: "Оформление заказа", value: 5073, fill: "var(--color-checkout)" },
  { stage: "Покупка", value: 1928, fill: "var(--color-purchase)" },
];

// Источники трафика
const trafficSourcesData = [
  { source: "organic", name: "Органический поиск", visitors: 18540, fill: "var(--color-organic)" },
  { source: "direct", name: "Прямой заход", visitors: 12680, fill: "var(--color-direct)" },
  { source: "social", name: "Соцсети", visitors: 9450, fill: "var(--color-social)" },
  { source: "email", name: "Email рассылки", visitors: 6820, fill: "var(--color-email)" },
  { source: "ads", name: "Реклама", visitors: 5350, fill: "var(--color-ads)" },
];

// Продажи по регионам
const regionData = [
  { region: "Москва", revenue: 3250000, orders: 1024 },
  { region: "СПб", revenue: 1890000, orders: 612 },
  { region: "Новосибирск", revenue: 720000, orders: 245 },
  { region: "Екатеринбург", revenue: 680000, orders: 228 },
  { region: "Казань", revenue: 540000, orders: 185 },
  { region: "Краснодар", revenue: 480000, orders: 162 },
  { region: "Самара", revenue: 420000, orders: 142 },
  { region: "Другие", revenue: 940000, orders: 330 },
];

// ==================== КОНФИГУРАЦИИ ГРАФИКОВ ====================

const dailyChartConfig = {
  revenue: { label: "Выручка", color: "var(--chart-1)" },
  orders: { label: "Заказы", color: "var(--chart-2)" },
  visitors: { label: "Посетители", color: "var(--chart-3)" },
} satisfies ChartConfig;

const categoryChartConfig = {
  value: { label: "Выручка" },
  electronics: { label: "Электроника", color: "var(--chart-1)" },
  clothing: { label: "Одежда", color: "var(--chart-2)" },
  home: { label: "Дом и сад", color: "var(--chart-3)" },
  sports: { label: "Спорт", color: "var(--chart-4)" },
  beauty: { label: "Красота", color: "var(--chart-5)" },
} satisfies ChartConfig;

const topProductsChartConfig = {
  revenue: { label: "Выручка", color: "var(--chart-1)" },
  label: { color: "var(--background)" },
} satisfies ChartConfig;

const funnelChartConfig = {
  value: { label: "Количество" },
  visitors: { label: "Посетители", color: "var(--chart-1)" },
  views: { label: "Просмотры", color: "var(--chart-2)" },
  cart: { label: "Корзина", color: "var(--chart-3)" },
  checkout: { label: "Оформление", color: "var(--chart-4)" },
  purchase: { label: "Покупка", color: "var(--chart-5)" },
} satisfies ChartConfig;

const trafficChartConfig = {
  visitors: { label: "Посетители" },
  organic: { label: "Органика", color: "var(--chart-1)" },
  direct: { label: "Прямой", color: "var(--chart-2)" },
  social: { label: "Соцсети", color: "var(--chart-3)" },
  email: { label: "Email", color: "var(--chart-4)" },
  ads: { label: "Реклама", color: "var(--chart-5)" },
} satisfies ChartConfig;

const regionChartConfig = {
  revenue: { label: "Выручка", color: "var(--chart-1)" },
  orders: { label: "Заказы", color: "var(--chart-2)" },
} satisfies ChartConfig;

// ==================== КОМПОНЕНТ ====================

export default function DemoAnalytics() {
  const [activeMetric, setActiveMetric] = React.useState<"revenue" | "orders" | "visitors">("revenue");

  // Расчет метрик
  const totalRevenue = dailySalesData.reduce((sum, d) => sum + d.revenue, 0);
  const totalOrders = dailySalesData.reduce((sum, d) => sum + d.orders, 0);
  const totalVisitors = dailySalesData.reduce((sum, d) => sum + d.visitors, 0);
  const avgOrderValue = Math.round(totalRevenue / totalOrders);
  const conversionRate = ((totalOrders / totalVisitors) * 100).toFixed(2);

  // Сравнение с предыдущим периодом (первые 15 дней vs последние 15)
  const firstHalf = dailySalesData.slice(0, 15).reduce((sum, d) => sum + d.revenue, 0);
  const secondHalf = dailySalesData.slice(15).reduce((sum, d) => sum + d.revenue, 0);
  const growthPercent = Math.round(((secondHalf - firstHalf) / firstHalf) * 100);

  // План продаж
  const salesTarget = 7000000;
  const targetProgress = Math.round((totalRevenue / salesTarget) * 100);

  const metricTotals = React.useMemo(() => ({
    revenue: totalRevenue,
    orders: totalOrders,
    visitors: totalVisitors,
  }), [totalRevenue, totalOrders, totalVisitors]);

  const formatMetricValue = (key: string, value: number) => {
    if (key === "revenue") return `${(value / 1000000).toFixed(2)}M\u00A0₽`; // non-breaking space
    if (key === "visitors") return value.toLocaleString("ru-RU");
    return value.toLocaleString("ru-RU");
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="border-b bg-card">
        <div className="container mx-auto px-4 md:px-6 py-4 md:py-6">
          <h1 className="text-2xl md:text-3xl font-bold">E-commerce Аналитика</h1>
          <p className="text-muted-foreground mt-1">
            Демонстрационный дашборд с данными за декабрь 2024
          </p>
        </div>
      </div>

      {/* Content */}
      <div className="container mx-auto px-4 md:px-6 py-6 md:py-8 space-y-6">

        {/* KPI Cards */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Выручка
              </CardTitle>
              <DollarSign className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {(totalRevenue / 1000000).toFixed(2)}M ₽
              </div>
              <div className="flex items-center gap-1 text-xs mt-1">
                {growthPercent > 0 ? (
                  <>
                    <TrendingUp className="h-3 w-3 text-green-500" />
                    <span className="text-green-500">+{growthPercent}%</span>
                  </>
                ) : (
                  <>
                    <TrendingDown className="h-3 w-3 text-red-500" />
                    <span className="text-red-500">{growthPercent}%</span>
                  </>
                )}
                <span className="text-muted-foreground">vs пред. период</span>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Заказы
              </CardTitle>
              <ShoppingCart className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {totalOrders.toLocaleString("ru-RU")}
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                Средний чек: {avgOrderValue.toLocaleString("ru-RU")} ₽
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Посетители
              </CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {totalVisitors.toLocaleString("ru-RU")}
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                Конверсия: {conversionRate}%
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                План продаж
              </CardTitle>
              <Package className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {targetProgress}%
              </div>
              <div className="w-full bg-muted rounded-full h-2 mt-2">
                <div
                  className="bg-primary h-2 rounded-full"
                  style={{ width: `${Math.min(targetProgress, 100)}%` }}
                />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Chart - Daily Metrics with Toggle */}
        <Card>
          <CardHeader className="flex flex-col items-stretch border-b !p-0 sm:flex-row">
            <div className="flex flex-1 flex-col justify-center gap-1 px-6 py-5">
              <CardTitle>Динамика за 30 дней</CardTitle>
              <CardDescription>Выберите метрику для детального анализа</CardDescription>
            </div>
            <div className="flex">
              {(["revenue", "orders", "visitors"] as const).map((key) => (
                <button
                  key={key}
                  data-active={activeMetric === key}
                  className="data-[active=true]:bg-muted/50 relative flex flex-1 flex-col justify-center gap-1 border-t px-4 py-3 text-left even:border-l sm:border-l sm:border-t-0 sm:px-6 sm:py-4"
                  onClick={() => setActiveMetric(key)}
                >
                  <span className="text-xs text-muted-foreground">
                    {dailyChartConfig[key].label}
                  </span>
                  <span className="text-lg font-bold leading-none sm:text-2xl whitespace-nowrap">
                    {formatMetricValue(key, metricTotals[key])}
                  </span>
                </button>
              ))}
            </div>
          </CardHeader>
          <CardContent className="px-2 pt-4 sm:px-6 sm:pt-6">
            <ChartContainer config={dailyChartConfig} className="aspect-auto h-[300px] w-full">
              <AreaChart data={dailySalesData} margin={{ left: 12, right: 12, top: 12 }}>
                <defs>
                  <linearGradient id="fillMetric" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor={`var(--color-${activeMetric})`} stopOpacity={0.8} />
                    <stop offset="95%" stopColor={`var(--color-${activeMetric})`} stopOpacity={0.1} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" tickLine={false} axisLine={false} tickMargin={8} />
                <YAxis
                  tickLine={false}
                  axisLine={false}
                  tickMargin={8}
                  tickFormatter={(value) =>
                    activeMetric === "revenue"
                      ? `${(value / 1000).toFixed(0)}k`
                      : value.toString()
                  }
                />
                <ChartTooltip
                  content={
                    <ChartTooltipContent
                      formatter={(value, name) => {
                        const v = Number(value);
                        if (name === "revenue") return [`${v.toLocaleString("ru-RU")} ₽`, "Выручка"];
                        if (name === "orders") return [`${v} шт`, "Заказы"];
                        return [`${v.toLocaleString("ru-RU")}`, "Посетители"];
                      }}
                    />
                  }
                />
                <Area
                  dataKey={activeMetric}
                  type="monotone"
                  fill="url(#fillMetric)"
                  stroke={`var(--color-${activeMetric})`}
                  strokeWidth={2}
                />
              </AreaChart>
            </ChartContainer>
          </CardContent>
        </Card>

        {/* Second Row - Categories & Top Products */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Category Pie Chart */}
          <Card>
            <CardHeader>
              <CardTitle>Продажи по категориям</CardTitle>
              <CardDescription>Распределение выручки</CardDescription>
            </CardHeader>
            <CardContent>
              <ChartContainer config={categoryChartConfig} className="mx-auto aspect-square max-h-[300px]">
                <PieChart>
                  <ChartTooltip
                    content={
                      <ChartTooltipContent
                        formatter={(value) => [`${(Number(value) / 1000000).toFixed(2)}M ₽`, "Выручка"]}
                      />
                    }
                  />
                  <Pie
                    data={categoryData}
                    dataKey="value"
                    nameKey="name"
                    innerRadius={60}
                    strokeWidth={5}
                  >
                    <Label
                      content={({ viewBox }) => {
                        if (viewBox && "cx" in viewBox && "cy" in viewBox) {
                          const total = categoryData.reduce((sum, d) => sum + d.value, 0);
                          return (
                            <text x={viewBox.cx} y={viewBox.cy} textAnchor="middle" dominantBaseline="middle">
                              <tspan x={viewBox.cx} y={viewBox.cy} className="fill-foreground text-2xl font-bold">
                                {(total / 1000000).toFixed(1)}M
                              </tspan>
                              <tspan x={viewBox.cx} y={(viewBox.cy || 0) + 20} className="fill-muted-foreground text-sm">
                                Всего
                              </tspan>
                            </text>
                          );
                        }
                      }}
                    />
                  </Pie>
                  <ChartLegend
                    content={<ChartLegendContent nameKey="category" />}
                    className="-translate-y-2 flex-wrap gap-2 *:basis-1/3 *:justify-center"
                  />
                </PieChart>
              </ChartContainer>
            </CardContent>
          </Card>

          {/* Top Products Bar Chart */}
          <Card>
            <CardHeader>
              <CardTitle>Топ-10 товаров</CardTitle>
              <CardDescription>По выручке за период</CardDescription>
            </CardHeader>
            <CardContent>
              <ChartContainer config={topProductsChartConfig} className="h-[350px] w-full">
                <BarChart data={topProductsData} layout="vertical" margin={{ right: 60 }}>
                  <CartesianGrid horizontal={false} />
                  <YAxis
                    dataKey="product"
                    type="category"
                    tickLine={false}
                    axisLine={false}
                    width={100}
                    tick={{ fontSize: 11 }}
                  />
                  <XAxis dataKey="revenue" type="number" hide />
                  <ChartTooltip
                    content={
                      <ChartTooltipContent
                        formatter={(value, name, item) => [
                          `${Number(value).toLocaleString("ru-RU")} ₽ (${item.payload.units} шт)`,
                          "Выручка",
                        ]}
                      />
                    }
                  />
                  <Bar dataKey="revenue" fill="var(--color-revenue)" radius={4}>
                    <LabelList
                      dataKey="revenue"
                      position="right"
                      offset={8}
                      className="fill-foreground"
                      fontSize={11}
                      formatter={(value: number) => `${(value / 1000).toFixed(0)}k`}
                    />
                  </Bar>
                </BarChart>
              </ChartContainer>
            </CardContent>
          </Card>
        </div>

        {/* Third Row - Funnel & Traffic Sources */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Funnel Chart */}
          <Card>
            <CardHeader>
              <CardTitle>Воронка конверсии</CardTitle>
              <CardDescription>От посетителя до покупки</CardDescription>
            </CardHeader>
            <CardContent>
              <ChartContainer config={funnelChartConfig} className="h-[300px] w-full">
                <BarChart data={funnelData} layout="vertical" margin={{ right: 80 }}>
                  <CartesianGrid horizontal={false} />
                  <YAxis
                    dataKey="stage"
                    type="category"
                    tickLine={false}
                    axisLine={false}
                    width={130}
                    tick={{ fontSize: 11 }}
                  />
                  <XAxis dataKey="value" type="number" hide />
                  <ChartTooltip
                    content={
                      <ChartTooltipContent
                        formatter={(value, name, item) => {
                          const idx = funnelData.findIndex((d) => d.stage === item.payload.stage);
                          const prevValue = idx > 0 ? funnelData[idx - 1].value : Number(value);
                          const convRate = ((Number(value) / prevValue) * 100).toFixed(1);
                          return [`${Number(value).toLocaleString("ru-RU")} (${convRate}% от пред.)`, ""];
                        }}
                      />
                    }
                  />
                  <Bar dataKey="value" radius={4}>
                    <LabelList
                      dataKey="value"
                      position="right"
                      offset={8}
                      className="fill-foreground"
                      fontSize={11}
                      formatter={(value: number) => value.toLocaleString("ru-RU")}
                    />
                  </Bar>
                </BarChart>
              </ChartContainer>
            </CardContent>
            <CardFooter className="text-sm text-muted-foreground">
              Общая конверсия: {((funnelData[4].value / funnelData[0].value) * 100).toFixed(2)}%
            </CardFooter>
          </Card>

          {/* Traffic Sources Pie */}
          <Card>
            <CardHeader>
              <CardTitle>Источники трафика</CardTitle>
              <CardDescription>Откуда приходят посетители</CardDescription>
            </CardHeader>
            <CardContent>
              <ChartContainer config={trafficChartConfig} className="mx-auto aspect-square max-h-[280px]">
                <PieChart>
                  <ChartTooltip
                    content={
                      <ChartTooltipContent
                        formatter={(value) => {
                          const total = trafficSourcesData.reduce((sum, d) => sum + d.visitors, 0);
                          const percent = ((Number(value) / total) * 100).toFixed(1);
                          return [`${Number(value).toLocaleString("ru-RU")} (${percent}%)`, "Посетители"];
                        }}
                      />
                    }
                  />
                  <Pie data={trafficSourcesData} dataKey="visitors" nameKey="name" />
                  <ChartLegend
                    content={<ChartLegendContent nameKey="source" />}
                    className="-translate-y-2 flex-wrap gap-2 *:basis-1/3 *:justify-center"
                  />
                </PieChart>
              </ChartContainer>
            </CardContent>
          </Card>
        </div>

        {/* Fourth Row - Regions */}
        <Card>
          <CardHeader>
            <CardTitle>Продажи по регионам</CardTitle>
            <CardDescription>Топ городов по выручке</CardDescription>
          </CardHeader>
          <CardContent>
            <ChartContainer config={regionChartConfig} className="h-[300px] w-full">
              <BarChart data={regionData} margin={{ top: 20 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="region" tickLine={false} axisLine={false} tick={{ fontSize: 11 }} />
                <YAxis
                  tickLine={false}
                  axisLine={false}
                  tickFormatter={(value) => `${(value / 1000000).toFixed(1)}M`}
                />
                <ChartTooltip
                  content={
                    <ChartTooltipContent
                      formatter={(value, name) => {
                        if (name === "revenue") return [`${Number(value).toLocaleString("ru-RU")} ₽`, "Выручка"];
                        return [`${value} шт`, "Заказы"];
                      }}
                    />
                  }
                />
                <Bar dataKey="revenue" fill="var(--color-revenue)" radius={[4, 4, 0, 0]}>
                  <LabelList
                    dataKey="revenue"
                    position="top"
                    offset={8}
                    className="fill-foreground"
                    fontSize={10}
                    formatter={(value: number) => `${(value / 1000000).toFixed(1)}M`}
                  />
                </Bar>
              </BarChart>
            </ChartContainer>
          </CardContent>
        </Card>

        {/* Footer */}
        <div className="text-center text-sm text-muted-foreground pt-4">
          Данные обновлены: 30 декабря 2024 | Демонстрационный дашборд
        </div>
      </div>
    </div>
  );
}
