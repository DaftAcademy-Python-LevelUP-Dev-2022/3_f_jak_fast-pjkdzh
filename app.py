import datetime

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
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

@app.post("/check/{name}/{date}", response_class=HTMLResponse)
def check(name: str, date: str):
    age = datetime.date.today() - datetime.date(date)
    return templates.TemplateResponse({"name": name, "age":age})
