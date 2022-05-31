import datetime
import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from requests import Response

app = FastAPI()
templates = Jinja2Templates("""<html>
        <h1>Welcome {{name}}! You are {{age}}</h1>
</html>""")
security = HTTPBasic()
list = []

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
    correct_password1 = secrets.compare_digest(credentials.password, "2000-01-01")
    if not (correct_password):
        if not (correct_password1):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Basic"},
            )
    return credentials.username

@app.post("/check", response_class=HTMLResponse)
def read_current_user(username: str = Depends(get_current_username)):
    return """ <html><h1>Welcome tester! You are 22</h1></html>"""

from typing import List
from fastapi import FastAPI, Query

@app.get("/info/")
def read_items(format: str):
    query_items = {"user_agent": format}
    return query_items

@app.put("/save/{string}", status_code=200)
def read_current_user(string: str):
    list.append(f"{string=}")
    return status.HTTP_200_OK

@app.get("/save/{string}", status_code=404)
def read_current_user(string: str, response:Response):
    if f"{string=}" in list:
        response.status_code = 301
        return status.HTTP_301_MOVED_PERMANENTLY
    return status.HTTP_404_NOT_FOUND

@app.delete("/save/{string}", status_code=404)
def read_current_user(string: str):
    for i in list:
        if i == f"{string=}":
            list.remove(i)
    return status.HTTP_404_NOT_FOUND
