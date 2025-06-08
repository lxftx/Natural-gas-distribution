<h1>🌐 Natural Gas Distribution</h1>
<p>Полноценное веб-приложение для расчета и визуализации оптимального распределения природного газа. Включает клиентскую и серверную части, реализующие авторизацию, сохранение истории и расчеты с использованием математических моделей.</p>
<h2>📁 Структура проекта</h2>
<ul>
   <li><strong>/client</strong> — интерфейс пользователя на React + TypeScript</li>
   <li><strong>/server</strong> — сервер на Django + DRF</li>
</ul>
<h2>🚀 Быстрый старт</h2>
<h3>1. Клонируйте репозиторий</h3>
<pre><code>git clone https://github.com/lxftx/Natural-gas-distribution.git
cd Natural-gas-distribution</code></pre>
<h3>2. Установка</h3>
<p>Создайте файл <code>.env</code> в корне проекта:</p>
<pre><code>DEBUG=True
LANGUAGE_CODE=ru
TIME_ZONE=Asia/Yekaterinburg
SECRET_KEY=django-insecure-4o@nxycbw)sa=s%r^ry-vvqrulez4#%ou9$4ya3w2(qb55(03a
DB_NAME=solver
DB_USER=admin
DB_PASS=admin
DB_HOST=database
DB_PORT=5432
VITE_API_URL=http://localhost:7000/api/
CLIENT_URLS=http://localhost:8000,http://127.0.0.1:8000</code></pre>
<h3>3. Установка и запуск сервера</h3>
<pre><code>docker compose build
docker compose run --rm server sh -c "python manage.py makemigrations && python manage.py migrate"
docker compose up</code></pre>
<h2>🔑 Авторизация</h2>
<p>Реализована регистрация, вход в систему и защита маршрутов для авторизованных пользователей.</p>
<h2>🧮 Расчет</h2>
<p>Пользователь вводит параметры задачи, сервер выполняет математические расчеты и возвращает результат. Доступна история расчетов.</p>
<h2>📘 Swagger API</h2>
<p>Документация API доступна по адресу:</p>
<pre><code>/swagger/</code></pre>
<h2>🛠️ Используемые технологии</h2>
<h3>Клиент</h3>
<ul>
   <li>React + TypeScript</li>
   <li>Vite</li>
   <li>Tailwind CSS</li>
   <li>Radix UI</li>
   <li>Context API для аутентификации</li>
</ul>
<h3>Сервер</h3>
<ul>
   <li>Django</li>
   <li>Django REST Framework</li>
   <li>JWT авторизация</li>
   <li>Swagger для API документации</li>
</ul>