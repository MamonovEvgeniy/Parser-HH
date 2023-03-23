
Используйте <code>requirements.txt</code> или подготовьте окружение самостоятельно, установив необходимые библиотеки:
<pre>
pip install requests
pip install bs4
pip install lxml
pip install fake_useragent
</pre>

___________________________________________________________

Скрипт запускатеся из консоли следующим образом:
python main.py

Скрипт-парсер поможет получить все удовлетворяющие запросу результаты, найденные на сайте hh.ru

Для изменения поискового запроса на сайте и предоставления результатов по нему необходимо заменить параметр с "python" на удовлетворяющий Вашему запросу параметр. Изначально скрипт написан для парсера по поисковому запросу python.

Результат выполнения скрипта записывается в файл data.json и содержит следующее:

•	Название вакансии;

•	Название компании;

•	Требуемый опыт;

•	Зарплата;

•	Теги;

•	Ссылка на вакансию.
