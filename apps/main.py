from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from apps.routers import plants, sensors, requirements, alerts, dashboard ,prediction


app = FastAPI(
    title="Smart Greenhouse API",
)



# Routers
app.include_router(
    plants.router,
    prefix="/plants",
    tags=["Plants"]
)

app.include_router(
    sensors.router,
    prefix="/sensors",
    tags=["Sensors"]
)

app.include_router(
    requirements.router,
    prefix="/requirements",
    tags=["Requirements"]
)

app.include_router(
    alerts.router,
    prefix="/alerts",
    tags=["Alerts"]
)

app.include_router(
    prediction.router,
    prefix="/prediction",
    tags=["Prediction"]
)

app.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["Dashboard"]
)


# Home page

app.mount(
    "/static",
    StaticFiles(directory="frontend"),
    name="static"
)


@app.get("/")
def home():
    return FileResponse(
        "frontend/index.html"
    )
