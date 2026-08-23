from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates

# from fastapi.responses import HTMLResponse, FileResponse
# from fastapi.templating import Jinja2Templates


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates= Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})
