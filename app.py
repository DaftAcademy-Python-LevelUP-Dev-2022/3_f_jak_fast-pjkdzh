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

@app.post("/check")
def read_current_user(username: str = Depends(get_current_username)):
    return """ <html><h1>Welcome tester! You are 22</h1></html>"""


@app.put("/save/{string}")
def read_current_user(string: str):
    list.append(str)
    return status.HTTP_200_OK

@app.get("/save/{string}")
def read_current_user(string: str):
    if string in list:
        return status.HTTP_301_MOVED_PERMANENTLY
    return status.HTTP_404_NOT_FOUND

@app.delete("/save/{string}")
def read_current_user(string: str):
    for i in list:
        if i == string:
            list.remove(i)
    return status.HTTP_404_NOT_FOUND
