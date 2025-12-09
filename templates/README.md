```markdown
# Документація API (lpnu_api)

Ця папка містить OpenAPI spec у YAML та JSON форматах і коротку інструкцію.

Файли:
- openapi.yaml — OpenAPI 3.0 (YAML)
- openapi.json — OpenAPI 3.0 (JSON)
- README.md — цей файл

Як це працює
1. Я додав маршрути у ваш app.py:
   - GET /openapi.yaml — повертає YAML
   - GET /openapi.json — повертає JSON
   - GET /docs/ — ReDoc UI (людям зручно переглядати)

2. Після пуша на репозиторій Render автоматично перезавантажить сервіс.
   Перевірте:
   - https://lpnu-api-py6o.onrender.com/openapi.yaml
   - https://lpnu-api-py6o.onrender.com/openapi.json
   - https://lpnu-api-py6o.onrender.com/docs/

Що віддати PythonAnywhere
- Рекомендую надати їм пряме посилання на YAML:
  https://lpnu-api-py6o.onrender.com/openapi.yaml
- Для людського перегляду додайте також:
  https://lpnu-api-py6o.onrender.com/docs/

Як оновлювати spec
- Якщо зміните /api/schedule або додасте нові маршрути — оновіть docs/openapi.yaml та docs/openapi.json.
- Можна автоматизувати генерацію spec (flask-apispec, apispec) та на CI перезаписувати файли у docs/.

Поради безпеки
- Файли документації повинні бути публічними, якщо PythonAnywhere має отримати їх за HTTP.
- Якщо ви не хочете робити їх постійно публічними — тимчасово дозвольте доступ або дайте PythonAnywhere IP для читання.

Якщо потрібно, можу:
- Згенерувати OpenAPI автоматично з коду (приклад з flask-apispec).
- Зробити PR у ваш репозиторій (повідомте owner/repo і гілку).
```