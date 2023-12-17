# data-storage-system

В этом проекте реализована отказоустойчивая система хранения для выдачи локальных датасетов в распределенных вычислительных системах. В качестве сервера использовался FastAPI с Unicorn и для прокси-сервера NGINX. Датасет может использоваться любой, в данном примере применялся набор данных с ренгеновскими изображениями рака легких.

# Архитектура

Сначала участник распределительных вычислений заходит в boinc клиент и добавляет проект добавляя ссылку, регистрируется и запускает получение заданий. После этого на сервер проекта приходит запрос в boinc server, где выдается задание для выполнения. Далее boinc client получив задание создает виртуальную среду, в которой запускается присланное задание. При выполнении задания отправляется запрос на получение списка изображений(локального датасета) для данной сессии. После того как список изображений в формате json будет получен, каждое изображение будет загружено поэтапно. Сначала обучающая выборка, затем валидационная, после тестовая.

# Структура репозитория

В репозитории вы найдете следующие папки:
1. Папка "app" располагает инструкции для NGINX;
2. Папка "images примеры и дополнительная информация";
3. Файл "docker-compose-ci.xaml" инструкции для поднятия кластера;
4. Файл "DockerFile" инстуркции для создания образа сервера;
5. Файл "pip.conf" SSL сертификаты для скачивания библиотек;
6. Файл "requirements.txt" список зависимостей

# Как запустить

1. Перейти в директории с проектом и выполнить команду по созданию образа "docker build -t unicorn-server ."
2. Поменять в volums(first-volume-data,second-volume-data,third-volume-data) путь к данным test, train, val в docker-compose-ci.yaml
3. Инициализировать swarm "docker swarm init"
4. Создать сеть "docker network create -d overlay custom"
5. Запустить развертывание "docker-compose -f docker-compose-ci.yaml up -d"

