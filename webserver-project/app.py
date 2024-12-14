from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setup(25, GPIO.OUT)  # Set GPIO pin 25 as output
SWITCH_PIN = 9 # input pin 9
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/activate-gpio")
async def activate_gpio():
    try:
        GPIO.output(25, GPIO.HIGH)  # Activate GPIO pin
        return JSONResponse(content={"message": "GPIO pin 25 activated!"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/deactivate-gpio")
async def deactivate_gpio():
    try:
        GPIO.output(25, GPIO.LOW)  # Deactivate GPIO pin
        return JSONResponse(content={"message": "GPIO pin 25 deactivated!"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@app.get("/switch-state")
async def get_switch_state():
    """Retrieve the current state of the switch."""
    try:
        # Check the current state of the switch
        state = "ON" if GPIO.input(SWITCH_PIN) == GPIO.LOW else "OFF"
        return JSONResponse(content={"switch_state": state})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)