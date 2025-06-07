<h1>Natural Gas Distribution — Клиент</h1>
<p>Клиентская часть на <strong>Vite + React</strong> (TypeScript), реализующая UI для:</p>
<ul>
   <li>Авторизации / регистрации пользователей</li>
   <li>Расчёта оптимального распределения газа по печам</li>
   <li>Истории сохранённых расчётов с возможностью просмотра / удаления</li>
</ul>
<h2>📦 Установка</h2>
<pre><code>
git clone https://github.com/lxftx/Natural-gas-distribution.git
cd Natural-gas-distribution
</code></pre>
<h2>⚙️ Конфигурация окружения</h2>
<p>Создайте файл <code>.env</code> в корне проекта:</p>
<pre><code>
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
<h2>🚀 Запуск</h2>
<pre><code>docker compose build
docker compose up
docker compose run --rm server sh -c "python manage.py makemigrations && python manage.py migrate"</code></pre>
<h2>🗂 Структура</h2>
<ul>
   <li>
      <code>src/pages</code> — страницы: 
      <ul>
         <li><code>/Auth</code> — форма входа/регистрации;</li>
         <li><code>/Solver</code> — главный калькулятор + история вычислений;</li>
      </ul>
   </li>
   <li><code>src/components</code> — UI-компоненты (кнопки, input, модалки и прочее);</li>
   <li><code>src/context/auth-context.tsx</code> — контекст авторизации;</li>
   <li><code>src/api/index.ts</code> — API-обёртка axios с интерсепторами;</li>
   <li><code>src/pages/Solver/components</code> — форма, история, ResultModal и типы;</li>
   <li><code>src/lib/types.ts</code> — общие TS-интерфейсы.</li>
</ul>
<h2>🎯 Как использовать</h2>
<ol>
   <li>Перейдите по <code>/login</code> и авторизуйтесь или зарегистрируйтесь.</li>
   <li>Вы попадёте на страницу <code>/solver</code>, где вводятся основные параметры.</li>
   <li>Кнопка «Рассчитать» запускает запрос к API и показывает результат в модалке.</li>
   <li>Если вы авторизованы, после расчёта автоматически сохраняется история.</li>
   <li>Вкладка «История» (доступна для авторизованных) отображает прошлые расчёты, их можно просмотреть или удалить.</li>
</ol>
<h2>🔐 Авторизация</h2>
<ul>
   <li>В Docker-коде axios добавлен <code>Authorization: Bearer &lt;token&gt;</code> для всех запросов.</li>
   <li>Контекст сохраняет токен в <code>localStorage</code>, и делает refresh при загрузке.</li>
   <li>В Header отображается кнопка «Войти» или имя пользователя + дропдаун с опцией «Выйти».</li>
</ul>
<h2>🛠️ Ключевые улучшения</h2>
<ul>
   <li>Плавное переключение между вкладками «Калькулятор» и «История».</li>
   <li>Управление формами с динамическим числом печей и автозаполнением.</li>
   <li>Глобальная обработка ошибок с выводом в модальные окна.</li>
   <li>Чистый, модульный UI, оформленный с Tailwind CSS.</li>
</ul>
<h2>🎯 Roadmap</h2>
<ul>
   <li>Расширить валидацию форм (чтобы N ≥ 1 и т.д.).</li>
   <li>Добавить прогрессивный индикатор загрузки и лоадеры.</li>
   <li>Ввести ролей пользователей (администратор / обычный).</li>
</ul>
<h2>📞 Контакты</h2>
<p>Если есть идеи, предложения или баги — пишите в GitHub Issues.</p>
<p style="text-align:center; margin-top:3rem;">Удачного пользования!</p>