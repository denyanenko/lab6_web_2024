from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.carRoutes import router as car_router
from fastapi.responses import FileResponse
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/static/{file_path:path}")
async def static_file(file_path: str):
    file_location = os.path.join("static", file_path)
    return FileResponse(file_location, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})


@app.get("/",  summary="Serve the index page", description="Returns the main HTML page (index.html) for the application.")
async def read_index():
    return FileResponse(os.path.join("static", "index.html"))


# Підключення маршрутів
app.include_router(car_router, prefix="/api")
