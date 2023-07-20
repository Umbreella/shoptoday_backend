import uvicorn

from app.app import get_asgi_application

app = get_asgi_application()

if __name__ == '__main__':
    uvicorn.run(app)
