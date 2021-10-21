## Support_test_project
  
Данный проект предназначен для предоставления интерфейса взаимодействия со службой техподдержки API.
Для развертывания данного приложения необходимо установить DOCKER(под LINUX или MAC OS) или DOCKER DESKTOP и запустить 
проект из директории Support_test_project командой:</br>
_docker-compose up -d_

После запуска приложения необходимо сделать подготвить статические файлыб выполнить миграцию БД и создать superuser 
следующими командами:

_docker-compose exec web python manage.py createsuperuser_<br />


