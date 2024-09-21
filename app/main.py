from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi_keycloak import FastAPIKeycloak
from fastapi.templating import Jinja2Templates


app = FastAPI()


# Set up templates for rendering HTML
templates = Jinja2Templates(directory="templates")


# Initialize Keycloak
keycloak = FastAPIKeycloak(
    server_url="http://localhost:8080/auth/",
    client_id="truchuynh",
    client_secret="truc",
    realm="orange-team-realm",
    admin_client_secret="your-admin-client-secret",
    callback_uri="http://localhost:8000/callback"
)
app.mount("/auth", keycloak.router)


# Login page
@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# Callback endpoint to handle Keycloak response
@app.get("/callback")
async def callback(code: str, request: Request):
    token = keycloak.exchange_code_for_token(code)
    if token:
        response = RedirectResponse(url="/protected")
        response.set_cookie(key="Authorization", value=f"Bearer {token['access_token']}")
        return response
    return RedirectResponse(url="/login")


# Protected route example
@app.get("/protected")
async def protected_route(request: Request, token: str = Depends(keycloak.get_current_user)):
    return {"message": f"Welcome, {token['preferred_username']}"}


# Logout route
@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("Authorization")
    return response

#
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
