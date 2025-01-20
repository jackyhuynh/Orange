from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates


app = FastAPI()


# Set up templates for rendering HTML
templates = Jinja2Templates(directory='app/templates')


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# Login page
@app.get("/index")
async def index():
    return {"message": "Hello World"}


@app.get("/user/{name}")
async def user(name: str):
    return {"message": f"Hello {name}"}