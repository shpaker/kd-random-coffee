#весь этот файл нам нужен чтобы просто получить FastAPI
from typing import Union
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

uvicorn.run(app)

#Объяснение:
#Создание экземпляра FastAPI: app = FastAPI() создает экземпляр FastAPI приложения.
#Добавление маршрутов:
#app.include_router(users_views.router) добавляет маршруты из модуля users_views.
#app.include_router(clubs_views.router) добавляет маршруты из модуля clubs_views.
#app.include_router(user_club_views.router) добавляет маршруты из модуля user_club_views.
#Базовые маршруты:
#@app.get("/") и @app.get("/items/{item_id}") добавляют базовые маршруты к приложению.
#Запуск приложения:
#uvicorn.run(app, host="0.0.0.0", port=8000) запускает сервер Uvicorn с созданным приложением.
#Заключение:
#Использование app.include_router в файле __main__.py позволяет добавлять маршруты из других модулей в основное приложение FastAPI. 
#Это улучшает организацию кода и позволяет разделить логику маршрутов по разным файлам и модулям. 
#Таким образом, файл __main__.py остается чистым и сосредоточенным на запуске приложения, 
#в то время как логика маршрутов находится в соответствующих модулях.
