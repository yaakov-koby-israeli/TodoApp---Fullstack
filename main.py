from fastapi import FastAPI, Request, status
from .models import Base
from .database import engine
from .routers import auth , todos , admin , users
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

Base.metadata.create_all(bind=engine) # creating the db -- will run only if db does not exist

# 4 html
# templates = Jinja2Templates(directory="TODOAPP/templates")

# 4 css + js
app.mount("/static",StaticFiles(directory="TODOAPP/static"),name="static")


@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)
    # return templates.TemplateResponse("home.html",{"request": request})

# check if app is running
@app.get("/healthy")
def health_check():
    return {'status':'Healthy'}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)



