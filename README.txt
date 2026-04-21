Job Platform — готовый учебный Django-проект.

Что есть:
- регистрация: worker / employer
- красивые страницы login / register
- меню слева, аккаунт справа
- worker: создание и редактирование резюме
- employer: поиск, избранное, уведомления
- like работодателя создает уведомление работнику
- страна фиксирована: Қазақстан
- динамические поля в форме резюме

Как запустить:
1) cd job_platform_full_ready
2) python3 -m venv venv
3) source venv/bin/activate
4) pip install -r requirements.txt
5) python manage.py migrate
6) python manage.py runserver

Логины через Google / Apple / Phone — demo-кнопки интерфейса.
Полная рабочая регистрация идет через email/login/password.
