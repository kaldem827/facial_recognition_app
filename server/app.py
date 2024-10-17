from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from server.routers.fetch import fetch_info_router  # Importing your custom router
import os
# Create the main FastAPI app
app = FastAPI()
# Get the absolute path to the 'static' directory
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir,  "static")
template_dir = os.path.join(current_dir,  "templates")

# Mount static files (CSS, JS)
app.mount("/static", StaticFiles(directory=static_dir), name="static")
# Register routers

templates = Jinja2Templates(directory=template_dir)
app.include_router(fetch_info_router)  # Register fetch info router

@app.get("/", response_class=HTMLResponse)
async def add_user_form(request: Request):
    """
    Serve the Add User HTML form.
    """
    return templates.TemplateResponse("user_form.html", {"request": request})
