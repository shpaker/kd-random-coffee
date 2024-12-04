from .users_views import router as users_router
from .clubs_views import router as clubs_router
from .user_club_views import router as user_club_router
#Создаем отдельные файлы для каждого типа маршрутов:
#users_views.py — для маршрутов, связанных с пользователями.
#clubs_views.py — для маршрутов, связанных с клубами.
#user_club_views.py — для маршрутов, связанных с участием пользователей в клубах.
#В каждом файле создаем маршруты:
#Например, в users_views.py мы создаем маршруты для получения информации о пользователе и создания нового пользователя.
#Импортируем маршруты в основной файл приложения:
#В файле __main__.py мы импортируем маршруты из этих файлов и добавляем их в основное приложение FastAPI.