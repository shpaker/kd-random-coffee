import uvicorn

from random_coffee_be_versia10.main import make_app

if __name__ == "__main__":
    app = make_app()
    uvicorn.run(app)
