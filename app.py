
import datetime
import secrets
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import RedirectResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()
list = []
@app.get("/start", response_class=HTMLResponse)
def start():
    return """
    <html>
        <h1>The unix epoch started at 1970-01-01</h1>
    </html>
    """

def user_age(date: str) -> int:
    # try:
    birth_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    # except ValueError:
    #     return -1

    # if birth_date > datetime.datetime.today():
    #     return null

    return (datetime.datetime.today() - birth_date).days // 365


@app.post("/check", response_class=HTMLResponse)
def login(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    name = credentials.username
    age = user_age(credentials.password)

    if age < 16:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return templates.TemplateResponse(
        name='age.html.j2',
        context={'request': request, 'name': name, 'age': age},
        status_code=status.HTTP_200_OK
    )

@app.get("/info")
def info(request: Request, format=None):
    if not format:
        pass

    elif format.lower() == 'json':
        return {'user_agent': request.headers.get('User-Agent')}

    elif format.lower() == 'html':
        return templates.TemplateResponse(
            name='format.html.j2',
            context={'request': request, 'value': request.headers.get('User-Agent')}
        )

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Wrong format')

@app.put("/save/{string}", status_code=200)
def read_current_user(string: str):
    list.append(f"{string=}")
    return status.HTTP_200_OK

@app.get("/save/{string}", status_code=404)
def read_current_user(string: str):
    if f"{string=}" in list:
        return RedirectResponse(url='/info', status_code=status.HTTP_301_MOVED_PERMANENTLY)
    return status.HTTP_404_NOT_FOUND

@app.delete("/save/{string}", status_code=200)
def read_current_user(string: str):
    for i in list:
        if i == f"{string=}":
            list.remove(i)
    return status.HTTP_404_NOT_FOUND