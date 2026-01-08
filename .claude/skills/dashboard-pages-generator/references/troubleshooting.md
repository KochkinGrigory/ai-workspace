# Troubleshooting дашбордов

---

## Ссылка не работает (404)

**Проверить:**
1. Папка создана: `ls apps/dashboard-pages/frontend/src/app/`
2. Файл `page.tsx` существует внутри папки
3. Docker работает: `docker ps | grep dashboard`
4. **Перезапустить Docker** (самая частая причина!):
   ```bash
   cd /opt/ai-workspace/apps/dashboard-pages && docker-compose restart
   ```

---

## Порт 3001 занят

```
Error: address already in use 0.0.0.0:3001
```

**Решение:**
```bash
lsof -ti:3001 | xargs kill -9
cd /opt/ai-workspace/apps/dashboard-pages && docker-compose restart
```

---

## Изменения не применились

**Полный rebuild:**
```bash
cd /opt/ai-workspace/apps/dashboard-pages
docker-compose down
docker-compose up -d --build
```

---

## Проверка после рестарта

```bash
# Контейнер запущен?
docker ps | grep dashboard-frontend

# Страница отвечает?
curl -I https://my-jarvis.ru/dashboard/[report-name]
# Должен вернуть HTTP/1.1 200 OK
```

---

## Docker команды

```bash
# Перезапуск (после изменений в page.tsx)
docker-compose restart

# Полный rebuild (после package.json)
docker-compose down && docker-compose up -d --build

# Логи
docker-compose logs -f dashboard

# Статус
docker ps | grep dashboard
```
