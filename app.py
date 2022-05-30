import datetime
import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
templates = Jinja2Templates("""<html>
        <h1>Welcome {{name}}! You are {{age}}</h1>
</html>""")
security = HTTPBasic()


@app.get("/start", response_class=HTMLResponse)
def start():
    return """
    <html>
        <h1>The unix epoch started at 1970-01-01</h1>
    </html>
    """

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "tester")
    correct_password = secrets.compare_digest(credentials.password, "1990-01-01")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.post("/check")
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}
#
# @app.get("/check", response_class=HTMLResponse)
# def check(name: str, date: str):
#     age = datetime.date.today() - datetime.date(date)
#     return templates.TemplateResponse({"name": name, "age": "16"})
