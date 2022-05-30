import datetime
import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()
templates = Jinja2Templates("""<html>
        <h1>Welcome {{name}}! You are {{age}}</h1>
</html>""")


@app.get("/start", response_class=HTMLResponse)
def start():
    return """
    <html>
        <h1>The unix epoch started at 1970-01-01</h1>
    </html>
    """

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_date = secrets.compare_digest(datetime.date.today() - datetime.date(credentials.username), 16)
    if 16 > (correct_date):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/check")
def read_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    return templates.TemplateResponse({"name": credentials.username, "age": datetime.date.today() - datetime.date(credentials.username)})
#
# @app.get("/check", response_class=HTMLResponse)
# def check(name: str, date: str):
#     age = datetime.date.today() - datetime.date(date)
#     return templates.TemplateResponse({"name": name, "age": "16"})
