from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates
from apps.routers import plants,sensors,requirements


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates= Jinja2Templates(directory="templates")


app.include_router(
    plants.router,
    prefix="/plants",
    tags=["plants"]
)

app.include_router(
    sensors.router,
    prefix="/sensors",
    tags=["sensors"]
)

app.include_router(
    requirements.router,
    prefix="/requirements",
    tags=["requirements"]
)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})
