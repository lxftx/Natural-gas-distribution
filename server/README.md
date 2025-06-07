<h1>Natural Gas Distribution — Сервер</h1>
<p><strong>Django Rest Framework</strong>-приложение, реализующее backend-сервер с REST API для:</p>
<ul>
   <li>регистрации и авторизации пользователей (с токенами)</li>
   <li>обработки расчетов газораспределения</li>
   <li>сохранения истории запросов</li>
   <li>возврата результатов клиенту</li>
</ul>
<h2>📦 Установка</h2>
<p>Клонируйте репозиторий</p>
<pre><code>
git clone https://github.com/lxftx/Natural-gas-distribution.git
cd Natural-gas-distribution
</code></pre>
<h2>⚙️ Конфигурация окружения</h2>
<p>Создайте файл <code>.env</code> в корне проекта:</p>
<code><pre>
DEBUG=True
LANGUAGE_CODE=ru
TIME_ZONE=Asia/Yekaterinburg
SECRET_KEY=django-insecure-4o@nxycbw)sa=s%r^ry-vvqrulez4#%ou9$4ya3w2(qb55(03a
DB_NAME=solver
DB_USER=admin
DB_PASS=admin
DB_HOST=database
DB_PORT=5432
VITE_API_URL=http://localhost:7000/api/
CLIENT_URLS=http://localhost:8000,http://127.0.0.1:8000
</code></pre>
<h2>🗄️ Структура проекта</h2>
<ul>
   <li><code>server/</code> — основная конфигурация проекта</li>
   <li><code>user/</code> — регистрация, логин, сериализаторы, токены</li>
   <li><code>gas/</code> — модель истории расчетов, логика оптимизации</li>
</ul>
<h2>🚀 Запуск</h2>
<pre><code>docker compose build
docker compose up
docker compose run --rm server sh -c "python manage.py makemigrations && python manage.py migrate"</code></pre>
<h2>🔐 Авторизация</h2>
<p>JWT через библиотеку <code>SimpleJWT</code>. Используются access и refresh токены:</p>
<ul>
   <li><code>/api/user/login/</code> — получение токена</li>
   <li><code>/api/user/refresh/</code> — обновление access токена</li>
   <li><code>/api/user/register/</code> — регистрация нового пользователя</li>
   <li><code>/api/user/info/</code> — информация о текущем пользователе</li>
</ul>
<h2>🧠 Расчёты</h2>
<p>Оптимизация происходит в <code>gas/services.py</code>. После успешного запроса расчет сохраняется в БД (если пользователь авторизован).</p>
<h2>📘 Swagger-документация</h2>
<p>Автоматически доступна по адресу: <code>/swagger/</code> после запуска сервера. Включает все методы API с примерами запросов.</p>
<h2>🛡️ Безопасность</h2>
<ul>
   <li>Cookie настроены как <code>Secure + SameSite=None</code> для работы с CORS</li>
   <li>Токены не сохраняются в БД</li>
   <li>Доступ к истории и расчетам только для авторизованных пользователей</li>
</ul>
<h2>🔧 Возможные улучшения</h2>
<ul>
   <li>Добавить Celery для асинхронных расчетов</li>
   <li>Вынести optimizer в отдельный сервис (FastAPI / Python Worker)</li>
   <li>Расширить API логами, статусами и мета-данными</li>
</ul>
<h2>📎 Ссылки</h2>
<ul>
   <li><a href="https://github.com/lxftx/Natural-gas-distribution">Основной репозиторий проекта</a></li>
   <li><a href="https://github.com/lxftx/Natural-gas-distribution/tree/main/client">Клиентская часть</a></li>
</ul>
<p style="text-align:center; margin-top:3rem;">Сделано с ❤️ и Python</p>