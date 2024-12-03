from random_coffee_be.main import make_app
import uvicorn


if __name__ == '__main__':
    app = make_app()
    uvicorn.run(app)
