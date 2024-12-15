from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setup(25, GPIO.OUT)  # Set GPIO pin 25 as output
SWITCH_PIN = 9  # Input pin 9
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# FastAPI app initialization
app = FastAPI()

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="your-strong-secret-key")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# User credentials
USER_CREDENTIALS = {"haak": "haak"}

def get_current_user(request: Request):
    """Retrieve the current logged-in user from the session."""
    username = request.session.get("username")
    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized. Please log in.")
    return username

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Login screen if not logged in, otherwise redirect to index.html."""
    if "username" in request.session:
        return RedirectResponse("/index.html")
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    """Handle user login."""
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        request.session["username"] = username  # Set the session username
        return RedirectResponse("/index.html", status_code=302)  # Redirect to index.html after login
    return templates.TemplateResponse(
        "login.html", {"request": request, "error": "Invalid username or password"}
    )

@app.get("/logout")
async def logout(request: Request):
    """Log the user out by clearing the session."""
    request.session.clear()  # Clear session data
    return RedirectResponse("/", status_code=302)  # Redirect to the login page

@app.get("/index.html", response_class=HTMLResponse)
async def index(request: Request, username: str = Depends(get_current_user)):
    """Serve the same page as the root endpoint (/)."""
    return templates.TemplateResponse("index.html", {"request": request, "username": username})

@app.post("/activate-gpio")
async def activate_gpio(username: str = Depends(get_current_user)):
    """Activate GPIO pin with session-based authentication."""
    try:
        GPIO.output(25, GPIO.HIGH)  # Activate GPIO pin
        return JSONResponse(content={"message": f"GPIO pin 25 activated by {username}!"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/deactivate-gpio")
async def deactivate_gpio(username: str = Depends(get_current_user)):
    """Deactivate GPIO pin with session-based authentication."""
    try:
        GPIO.output(25, GPIO.LOW)  # Deactivate GPIO pin
        return JSONResponse(content={"message": f"GPIO pin 25 deactivated by {username}!"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/switch-state")
async def get_switch_state(username: str = Depends(get_current_user)):
    """Retrieve the current state of the switch with session-based authentication."""
    try:
        state = "ON" if GPIO.input(SWITCH_PIN) == GPIO.LOW else "OFF"
        return JSONResponse(content={"switch_state": state, "checked_by": username})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
