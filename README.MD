# Antonio Mele | Django 2 - blog
> Książka Antonio Mele pod tytułem "Django 2 - praktyczne tworzenie aplikacji sieciowych."
> Przepracowana dla wersji Django 2.2.7 w Pythonie 3.5.4

### Rozdział 1 - Utworzenie aplikacji bloga

##### 1.1 Instalowanie Django 
```pip install Django==2.2.7```

Wersję django w konsoli Pythona sprawdzam poleceniem:

```
>>> import django
>>> django.get_version()
```

##### 1.2 Tworzenie pierwszego projektu
`django-admin startproject mysite .`

##### 1.3 Utworzenie aplikacji

```
py manage.py startapp blog
py manage.py migrate
```