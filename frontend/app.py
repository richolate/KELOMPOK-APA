from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI()

# Static and template
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
@app.get("/login.html")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/do_login")
async def do_login():
    response = RedirectResponse(url="/users")
    response.set_cookie("is_logged_in", "true")
    return response

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login.html")
    response.delete_cookie("is_logged_in")  # penting: hapus cookie login
    return response

@app.get("/users")
@app.get("/users.html")
async def users_page(request: Request):
    if request.cookies.get("is_logged_in") != "true":
        return RedirectResponse(url="/login.html")
    return templates.TemplateResponse("users.html", {"request": request})

@app.get("/payment")
async def payment_page(request: Request):
    if request.cookies.get("is_logged_in") != "true":
        return RedirectResponse(url="/login.html")
    return templates.TemplateResponse("payment.html", {"request": request})

@app.get("/vendor")
@app.get("/vendors")
@app.get("/vendors.html")
async def vendors_page(request: Request):
    if request.cookies.get("is_logged_in") != "true":
        return RedirectResponse(url="/login.html")
    return templates.TemplateResponse("vendors.html", {"request": request})

@app.get("/products")
@app.get("/products.html")
async def products_page(request: Request):
    if request.cookies.get("is_logged_in") != "true":
        return RedirectResponse(url="/login.html")
    return templates.TemplateResponse("products.html", {"request": request})



# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)