from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.shorten import router as shorten_router
from app.api.redirect import router as redirect_router
from app.api.stats import router as stats_router

app = FastAPI()

# APIs (with prefixes)
app.include_router(shorten_router)
app.include_router(stats_router)

# 🔥 Redirect must be ROOT and LAST
app.include_router(redirect_router)

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

